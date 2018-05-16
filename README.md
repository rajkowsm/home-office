# home-office

Simple Python script that sends home office requests to your supervisor.
You can only request remote office for the current week and it must be done beforehand (no retroactive requests).

### Installation and config

Home-office script requires Python 2.7+.
You also need to create a config file:

```
config.ini
```

containing:

```ini
[email]
recipient=your.supervisor@company.com
cc=your.additional.supervisor.if.needed@com
sender=your.email@company.com
```

### Usage

```sh
python ho.py WEEKDAY
```

where `WEEKDAY` is abbreviated name of the weekday.