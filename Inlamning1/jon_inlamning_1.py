#Import my posts here
from RssArticles_1 import posts


##################### Extracting the Titles and Summaries ##################
def OnlyTitlesandSummaries():
    """
    This function should iterate through 'posts' and create a new list of dictionaries,
    each containing only 'title' and 'summary'. If either key is missing, replace it 
    with an empty string.
    
    Steps:
    1. Initialize an empty list: only_titles_and_summaries = []
    2. Loop over each item 'x' in posts.
       - Create a temporary dictionary `tempdict = {}`
       - Try to store x["title"] and x["summary"] in `tempdict`
         If a KeyError occurs, store "" (empty string) for that key instead.
       - Append tempdict to only_titles_and_summaries
    3. Return only_titles_and_summaries
    """
    
    only_titles_and_summaries = []
    
    for post in posts:
        tempdict = {}
        try:
            tempdict["title"] = post["title"]
        except KeyError:
            tempdict["title"] = ""

        try:
            tempdict["summary"] = post["summary"]
        except KeyError:
            tempdict["summary"] = ""

        only_titles_and_summaries.append(tempdict)

    return only_titles_and_summaries


def TitleAndSummaryList(only_titles_and_summaries):
    """
    This function should create a nested list, where each inner list contains one 
    combined string made by joining the title and summary for a single post.
    
    Steps:
    1. Initialize an empty list: title_and_summary_list = []
    2. For each dictionary in only_titles_and_summaries:
       - Extract its 'title' and 'summary'
       - Combine them in a single string, e.g., combined = title + " " + summary
       - Since we want a nested list of single-element lists, wrap this combined 
         string in a list, then append: title_and_summary_list.append([combined])
    3. Return title_and_summary_list
    """
    
    title_and_summary_list = []
    
    for item in only_titles_and_summaries:
        combined = item["title"] + " - " + item["summary"]
        title_and_summary_list.append([combined])

    return title_and_summary_list


def PrintDeposit(title_and_summary_list):
    """
    This function should flatten the list returned by TitleAndSummaryList into a 
    single list. That means if title_and_summary_list = [["Title1 Summary1"], ["Title2 Summary2"]],
    we want printdepositlist = ["Title1 Summary1", "Title2 Summary2"].
    
    Steps:
    1. Initialize an empty list: flattened_list = []
    2. Loop over each list in title_and_summary_list:
       - For each value in that nested list, append it to flattened_list
    3. Return flattened_list
    """
    
    flattened_list = []
    
    for item in title_and_summary_list:
        for value in item:
            flattened_list.append(value)

    return flattened_list


# -------------------- MAIN EXECUTION SECTION --------------------
if __name__ == "__main__":
    # 1. Extract only title and summary
    Only_the_titles_Summaries = OnlyTitlesandSummaries()

    # 2. Create nested lists of combined title+summary
    The_Title_Summary_List = TitleAndSummaryList(Only_the_titles_Summaries)

    # 3. Flatten and print the final result
    printdepositlist = PrintDeposit(The_Title_Summary_List)

    # Print to verify
    print(printdepositlist)