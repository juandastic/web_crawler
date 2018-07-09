# Crowl
The open-source SEO crawler.  
A crawler made by SEOs for SEOs, free and compatible with any operating system.  

## Setup

Crowl uses Python 3.6.4 and stores data into MySQL (for now).  
Create a MySQL user with the ability to create databases.  
Fill the `config.sample.ini` file and save it as `config.ini`.  

Install requirements:  

	pip install -r requirements.txt


## Usage

    python crowl.py -u https://www.crowl.tech/ -b crowltech  


Optional arguments:  
- `-u`, `--url`: Start URL (required)  
- `-b`, `--database`: Project basename for database creation (required in new crawl mode)  
- `-r`, `--resume`: Resume crawl using specified database (required in resume mode)  
- `-l`, `--links`: Store links (default: False)  
- `-c`, `--content`: Store page content (default: False)  
- `-d`, `--depth`: Maximum crawl depth (default: 5)  
- `--conf_file`: Path to config file (default: `config.ini`)  

__More examples:__  
Store links and content:  

    python crowl.py -u https://www.crowl.tech/ -b crowltech --links --content  

Crawl only 2 levels:  

    python crowl.py -u https://www.crowl.tech/ -b crowltech -d 2  

## Advanced configuration

For now, you can use Scrapy's advanced settings by editing the settings in `get_settings()` inside `crowl.py`.  
See [Scrapy documentation](https://doc.scrapy.org/en/latest/topics/settings.html) for more details on which settings are available.  

## Pausing and resuming crawls  

Crawls are automatically configured to be paused and resumed.  
To pause a crawl, simply stop the process (`ctrl`+`c`).  
You can resume a crawl by launching the crawler again with the `resume` argument.  

Example:  

    # Launch crawl
    python crowl.py -u https://www.crowl.tech/ -b crowltech  
    # Stop crawl using `ctrl`+`c`  
    # Resume crawl using Database ID  
    python crowl.py -u https://www.crowl.tech/ -r crowltech_20180624-164347  

