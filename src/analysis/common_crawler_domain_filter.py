import csv
import json
import tldextract

import os
import re

registered_domains = [
    "github.io",
    "google.com",
    "r2.dev",
    "bit.ly",
    "qrco.de",
    "cutt.ly",
    "t.co",
    "dweb.link",
    "ead.me",
    "q-r.to",
    "ipfs.io",
    "tinyurl.com",
    "is.gd",
    "urlz.fr",
    "cloudflare-ipfs.com",
    "rb.gy",
    "shorturl.at",
    "t.ly",
    "aragon.network",
    "on-fleek.app",
    "cf-ipfs.com",
    "webwave.dev",
    "ln.run",
    "ydns.eu",
    "s.id",
    "googleapis.com",
    "hoster-test.ru",
    "nxcli.io",
    "lighthouse.storage",
    "me2.do",
    "wl.co",
]

if __name__ == "__main__":
    for root, dirs, files in os.walk("/data/jxlu/common-crawl/CC-MAIN-2024-38"):
        pattern = re.compile(r"cdx-\d{5}$")
        filtered_files = [file for file in files if pattern.match(file)]
        print(filtered_files)
        for file in filtered_files:
            print(file)
            with open(f"/data/jxlu/common-crawl/CC-MAIN-2024-38/{file}", "r") as f:
                # lines = list(itertools.islice(f, 1))
                lines = f.readlines()
                lines = [line.strip("\n").split(" ", 2)[2] for line in lines]
                lines = [json.loads(line) for line in lines]
                lines = [[item["url"], item["status"]] for item in lines]

                result = {}
                url_registered_domains = set()

                for item in lines:
                    # print(item)
                    url = item[0]
                    url_registered_domain = tldextract.extract(url).registered_domain
                    url_registered_domains.add(url_registered_domain)
                    # print(url_registered_domain)
                    # if url_registered_domain in registered_domains:
                    #     if registered_domains not in result.keys():
                    #         result[registered_domains] = []
                    #     result[registered_domains].append(item)
                with open(
                    "/data/jxlu/common-crawl/results/test.csv", "w", newline=""
                ) as file:
                    writer = csv.writer(file)
                    print(url_registered_domains)
                    writer.writerows([[row] for row in list(url_registered_domains)])

                break

                # print(f"{file}: {len(result.keys())}")
                #
                # with open(f"/data/jxlu/common-crawl/results/{file}.json", "w") as f:
                #     f.write(json.dumps(result))
