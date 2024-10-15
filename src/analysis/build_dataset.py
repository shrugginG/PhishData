import json

with open(
    "/home/jxlu/project/PhishDetect/PhishData/data/specific_count_phishy_urls/100_with_top_domain_phishy_urls.json",
    "r",
) as f:
    origin_data = json.load(f)
    print(origin_data)

with open(
    "/home/jxlu/project/PhishDetect/PhishData/data/specific_count_phishy_urls/benign.txt",
    "w",
) as f1, open(
    "/home/jxlu/project/PhishDetect/PhishData/data/specific_count_phishy_urls/phishy.txt",
    "w",
) as f2:
    for item in origin_data:
        phishy_urls = [test[0] for test in item["phishy_urls"]]
        print(phishy_urls)
