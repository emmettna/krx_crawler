import json

parent_dir='krx/'

# Save to local storage
# rows: List[KrxPriceModel]
# parent_dir_path: Path to directory of download location
# name_post_fix: Name which may be added after date
# File name ex: 
# - without postfix: ./2021-11-01.json
# - with postfix:    ./2021-11-01-some_post_fix_name.json
async def save_to_local(rows:list, parent_dir_path: str, name_post_fix: str = ''):
    if len(rows) != 0:
        if name_post_fix != '':
            name_post_fix = '-'+name_post_fix
        # with open('krx/stock/' + rows[0].date.strftime("%Y-%m-%d")  + '.json', 'w') as f:
        with open(parent_dir_path + '/' + rows[0].date.strftime("%Y-%m-%d") + name_post_fix + '.json', 'w') as f:
            json.dump([r.to_dict() for r in rows], f, ensure_ascii=False)