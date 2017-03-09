from collections import defaultdict
import re
# from pprint import pprint
from bs4 import BeautifulSoup
from pelican import signals
from pelican.generators import ArticlesGenerator

# Notes
#   - Requires BeautifulSoup HTML parser:
#     https://www.crummy.com/software/BeautifulSoup/
#   - It is assumed that articles are generated before pages, i.e. that
#     the article_generator_finalized signal is fired before the
#     page_generator_finalized signal is fired.

tags_to_articles = defaultdict(list)

def record_tag_article_mapping(article_generator):
  # print("[print_article_info]")
  for article in article_generator.articles:
    for tag in article.tags:
      # print("tag = {}".format(tag.name))
      tags_to_articles[tag.name].append(article)

def print_page_info(page_generator):
  # print("[print_page_info]")
  # pprint(page_generator.context)
  # print("tags_to_articles = {}".format(tags_to_articles))
  for page in page_generator.pages:
    # print("--------- old content ---------")
    # print(page._content)
    # print("--------- processing ... ---------")
    # print("  SITEURL = {}".format(page_generator.context['SITEURL']))
    soup = BeautifulSoup(page._content, 'html.parser')
    for hook in soup.find_all("p", string=re.compile("{{\$ article_list .* \$}}")):
      match = re.search("{{\$ article_list ([^\s]+) \$}}", hook.string)
      groupingTagName = match.group(1)
      # print("Grouping by tag {}".format(groupingTagName))
      if len(tags_to_articles[groupingTagName]) > 0:
        ul = soup.new_tag("ul", **{"class": "article-lists-group"})
        hook.replace_with(ul)
        for article in tags_to_articles[groupingTagName]:
          # print("  title = {}".format(article.title))
          # print("  url = {}".format(article.url))
          # print("  save_as = {}".format(article.save_as))
          # print("  slug = {}".format(article.slug))
          a = soup.new_tag("a", href="{}/{}".format(page_generator.context['SITEURL'], article.url))
          a.string = article.title
          li = soup.new_tag("li", **{"class": "article-lists-item"})
          li.append(a)
          ul.append(li)

      page._content = str(soup)
      # print("--------- new content ---------")
      # print(page._content)

def register():
  # print("\n\n\n[ARTICLE-LISTS]")
  signals.article_generator_finalized.connect(record_tag_article_mapping)
  signals.page_generator_finalized.connect(print_page_info)
