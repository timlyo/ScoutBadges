import sys
import json
import datetime

from urllib3 import PoolManager

from bs4 import BeautifulSoup
import certifi

pages = {
	"beavers": "https://members.scouts.org.uk/supportresources/search/?cat=11,18",
	"cubs": "https://members.scouts.org.uk/supportresources/search/?cat=12,67",
	"scouts": "https://members.scouts.org.uk/supportresources/search/?cat=7,64",
	"explorers": "https://members.scouts.org.uk/supportresources/search/?cat=9,88",
}

pool = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def fix_url(url: str) -> str:
	"""adds host to url if missing"""
	if url.startswith("/"):
		url = "https://members.scouts.org.uk" + url
	return url


def get_html(url: str) -> BeautifulSoup:
	"""Get dom from url"""
	url = fix_url(url)
	html = pool.request("GET", url)
	return BeautifulSoup(html.data, "lxml")


def get_badge_urls(url: str) -> dict:
	"""Get list of urls on a unit's page"""
	data = get_html(url)
	urls = {}
	try:
		print("Parsing ", data.find("title"))
		urls["core_badges"] = data.find("a", string="Core badges")["href"]
		urls["activity_badges"] = data.find("a", string="Activity Badges")["href"]
		urls["staged_badges"] = data.find("a", string="Staged Activity Badges")["href"]
		urls["challenge_badges"] = data.find("a", string="Challenge Awards")["href"]

	except TypeError as e:
		if data.find("title") == "<title>Explorer Scout badges and awards</title>":
			urls["awards"] = data.find("a", string="Awards")["href"]
		else:
			print(e, file=sys.stderr)

	return urls


def parse_badge_lists(url: str) -> list:
	"""Go through the badges on a single page"""
	data = get_html(url)
	badges = []
	for badge in data.find_all("td"):
		badge_url = badge.find("a")["href"]
		badges.append(get_badge_info(badge_url))
	return badges


def get_badge_info(url: str) -> list:
	"""Get a single badge's information from a badge page """
	data = get_html(url)
	badge_section = data.find("div", {"class": "seven"})
	name = badge_section.find("h2").string
	image_url = fix_url(badge_section.find("img")["src"])
	print("\tgot ", name)
	return [name, image_url]


if __name__ == "__main__":
	badges = {"cubs": {"core_badges": [], "activity_badges": [], "staged_badges": [], "challenge_badges": []},
	          "scouts": {"core_badges": [], "activity_badges": [], "staged_badges": [], "challenge_badges": []},
	          "explorers": {"core_badges": [], "activity_badges": [], "staged_badges": [], "awards": []},
	          "beavers": {"core_badges": [], "activity_badges": [], "staged_badges": [], "challenge_badges": []}
	          }
	for group, page in pages.items():
		for key, url in get_badge_urls(page).items():
			badges[group][key] += parse_badge_lists(url)

	badges["last_update"] = datetime.datetime.utcnow().isoformat(" ")

	with open("badges.json", "w") as fp:
		json.dump(badges, fp)
