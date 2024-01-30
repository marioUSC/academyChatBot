from piazza_api import Piazza
import json

p = Piazza()
p.user_login()

class_profile = p.get_user_profile()['all_classes']

class_dic = {key: value["num"] for key, value in class_profile.items()}
print(f"Class list: {class_dic}")

class_id = input("Choose a course id from above: ")
num = int(input("Assign the number of posts: "))
print("Actual posts may be less than this number because some iterated posts are announcements & will not be displayed")
course = p.network(class_id)
course.get_post(num)
posts = course.iter_all_posts(limit=num)

post_dict = {}
for post in posts:

    if post['type'] == "question":
        post_detail = {"subject": post["history"][0]["subject"], "content": post["history"][0]["content"]}
        post_answers = post["children"]
        ans_dic = {}
        for answer in post_answers:
            if "history" in answer:
                # to do: multiple layers of followup
                ans_dic[answer["id"]] = answer["history"][0]["content"]
        post_dict[post["id"]] = {"time": post["created"], "detail": post_detail, "answers": ans_dic}

formatted_json = json.dumps(post_dict, indent=2)
# print(formatted_json)

# Choose a filename
filename = "piazza.json"

# Write the JSON string to the file
with open(filename, 'w') as file:
    file.write(formatted_json)

print(f"Data saved to {filename}")