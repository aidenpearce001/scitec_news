from loguru import logger
from config.settings import settings

with open(config_path, encoding="utf-8") as f:
    conf = yaml.safe_load(f)

def init_rss(conf: dict, update: bool=False, proxy_url=''):
    rss_list = []
    enabled = [{k: v} for k, v in conf.items() if v['enabled']]
    for rss in enabled:
        if update:
            if rss := update_rss(rss, proxy_url):
                rss_list.append(rss)
        else:
            (key, value), = rss.items()
            rss_list.append({key: root_path.joinpath(f'rss/{value["filename"]}')})

    feeds = []
    for rss in rss_list:
        (_, value), = rss.items()
        try:
            rss = listparser.parse(open(value,encoding="utf-8").read())
            for feed in rss.feeds:
                url = feed.url.strip().rstrip('/')
                short_url = url.split('://')[-1].split('www.')[-1]
                check = [feed for feed in feeds if short_url in feed]
                if not check:
                    feeds.append(url)
        except Exception as e:
            logger.warning(f"{value } fail due {e}")

    logger.success(f"{len(feeds)} feeds")

    return feeds