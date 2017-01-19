# A good Wunderlist robot just for myself

Since IFTTT doesn't support Wunderlist, and I need to add a task at a specific time ( Wunderlist just support date, not time ). So I write this.

I didn't implement the authorization part, so it's just for a developer with his own Wunderlist Apps.

Before you go, put your client id and access token in config.json. You can  get one [here](https://developer.wunderlist.com/apps).

To find out your list id, you can let the list_id empty in the config since you don't have it yet:
```bash
python wunderlist.py get_list
```

To add something, remember to put your:
```bash
python wunderlist.py add task_title
```
You can add `--due today/tomorrow/2038-01-19`, `--star`, `--list_id id` if you need.

I use it with [cron](https://en.wikipedia.org/wiki/Cron).