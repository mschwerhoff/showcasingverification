from collections import defaultdict
import re
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
  print("[print_page_info]")
  # print("tags_to_articles = {}".format(tags_to_articles))
  for page in page_generator.pages:
    if page.title == "DOOM":
      print("--------- old content ---------")
      print(page._content)
      print("--------- processing ... ---------")
      content = BeautifulSoup(page._content, 'html.parser')
      for hook in content.find_all("p", string=re.compile("{{\$ article_list .* \$}}")):
        # print(hook.string)
        match = re.search("{{\$ article_list ([^\s]+) \$}}", hook.string)
        groupingTag = match.group(1)
        print("Grouping by tag {}".format(groupingTag))
        for article in tags_to_articles[groupingTag]:
          print("  {}".format(article.title))
        
        hook.clear()
      print("--------- new content ---------")
      page._content = str(content)
      print(page._content)
    # if any(t.name == '' for t in page.tags):

# def on_all_content_generated(generators):
#   print("[on_all_content_generated]")
#   tags_to_articles = defaultdict(list)
#   for generator in generators:
#     if isinstance(generator, ArticlesGenerator):
#       for article in generator.articles:
#         for tag in article.tags:
#           # print("tag = {}".format(tag.name))
#           tags_to_articles[tag.name].append(article)
        
        

def register():
  # signals.all_generators_finalized.connect(on_all_content_generated)
  signals.article_generator_finalized.connect(record_tag_article_mapping)
  signals.page_generator_finalized.connect(print_page_info)
