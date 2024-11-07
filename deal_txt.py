lines = open("C:\\Users\\syske\\Downloads\\check_paper_info_1357169267568676954.sql").readlines()
paperIds = []
for line in lines:
    if line.startswith("--"):
        print(line)
        paperIds.append(line.replace('-- paper_id = ', '').replace('\n', ''))
print(len(paperIds), paperIds)