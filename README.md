# Reddit Api Utils

Reddit API is known to limit the total amount of recalled data to 1000 items. This is due to the following.

  - API is limited to using only what is cached in Casandra
  - User saved links are not saved kept past 1000 items
  - Reddit is ginormous and unforutnately cannot grow infinitely

After much frustration, thinking there issues in my scripts or even worse in the Reddit API, the issue was addressed by the mods of RedditDev in the below threads:

  - [RedditDev Comment Thread #1](https://www.reddit.com/r/redditdev/comments/30a7ap/does_reddit_api_limit_total_listings_returned_to/)
  - [RedditDev Comment Thread #2](https://www.reddit.com/r/redditdev/comments/2pvdfp/going_back_more_than_the_first_1000_posts_in_a/)

### Usage
```sh
$ python utils.py
```

### Dependencies

Reddit-API-Utils uses one open source projects to work properly:

* [Requests](http://www.python-requests.org/en/latest/) - HTTP for Humans!

### Installation

Needs python2.7+

```sh
$ git clone https://github.com/thelanman/reddit-api-utils
$ cd reddit-api-utils
$ touch saved_data.txt
```

### Todos

 - Support other parts of API beyond user saved links

License
----
MIT