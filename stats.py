import json
reviewers = {}
num_items = 0
num_items_with_reviews = 0
num_reviews = 0
stats = open("statistics.txt", "w")

with open('new_data.json') as json_file:
    data = json.load(json_file)
for i in data:
    for j in data[i]:
        num_items += 1
        if len(data[i][j]) > 0:
            num_items_with_reviews +=1
            for review in data[i][j]:
                num_reviews +=1
                if review['AuthorID'] in reviewers:
                    reviewers[review['AuthorID']] += 1
                else:
                    reviewers[review['AuthorID']] = 1


for i in reviewers:
    if i == "":
        num = reviewers[i]
        reviewers.pop(i)
        reviewers["Anonymous"] = num
#for i in reviewers:
#    print(i + ":" + str(reviewers[i]))



stats.write("Number of items: " + str(num_items) + '\n')
stats.write("Number of items with reviews: " + str(num_items_with_reviews) + '\n')
stats.write("Number of reviews: " + str(num_reviews) + '\n')
stats.write("Number of reviewers (non-anonymous): " + str(len(reviewers)) + '\n\n')
stats.write("AuthorID                    Number of Reviews\n")
for w in sorted(reviewers, key=reviewers.get,reverse=True):
    stats.write(w + "    " + str(reviewers[w]) + '\n')
print(num_items)
print(num_items_with_reviews)
print(num_reviews)