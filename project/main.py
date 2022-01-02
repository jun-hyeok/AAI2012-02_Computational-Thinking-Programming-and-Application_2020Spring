# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% import libraries
import requests  # for crawlering website
from bs4 import BeautifulSoup  # for parsing html.text
import re  # for regular expression
import csv  # for writnig and saving csv files

## ranking site URL main part
URL = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?"
# %% initiate, get_, print_, save_ objects <Movie class>
class Movie:
    ## you can receive parameter inputs at the same time as initialization
    ## or set parameter value to None first, recevie inputs after initiation, and update instances
    def __init__(self, rank=None, title=None, link=None, point=None):
        self.rank = rank  # rank of Movie
        self.title = title  # title of Movie
        self.link = link  # detailed page URL of Movie
        self.point = point  # score rated by netizen

    """ PRIVATE METHODS """
    ## crawl detaled page of Movie
    def _get_page(self):
        # request html of detailed page
        try:
            html = requests.get(self.link)
            return html
        # alert when error raised
        except requests.exceptions.RequestException:
            return print("Connection error or Invalid URL")

    ## parse html
    ## depends on ._get_page()
    def _get_soup(self):
        html = self._get_page()
        # select content from parsed html.text
        soup = BeautifulSoup(html.text, "html.parser").select_one("div#content")
        # parsing exception : login required on website
        # if nothing selected from parsed html.text, then return None
        if soup == None:
            print(f"Login required: {self.link}")
            return None
        else:
            return soup

    ## set instances(.summary, .director, .cast_main, .rate)
    ## depends on ._get_soup()
    def _get_info_spec(self):
        soup = self._get_soup()
        # break(return None) if soup is None : login required on website
        # set instances as "None" (to write in csv later)
        if soup is None:
            self.summary = "None"
            self.director = "None"
            self.cast_main = "None"
            self.rate = "None"
            return None
        # select info_spec from soup
        info_spec = soup.select("dl.info_spec > dd > p")
        # each film may or may not have a director
        # if info_spec has 4 fields, the film has a director
        if len(info_spec) == 4:
            # substitute commas(,) and whitespaces(\s+) in string using regular expression
            # then split the string
            self.summary = re.sub(
                r"\s+", ":", info_spec[0].text.replace(",", "").strip()
            ).split(":")
            # set instances
            self.director = info_spec[1].text
            self.cast_main = info_spec[2].text
            # remove "도움말" in string using regular expression
            self.rate = re.sub(
                r"\s+", " ", info_spec[3].text.replace("도움말", "").strip()
            )
        # if info_spec has 3 fields, the film does not have a director
        elif len(info_spec) == 3:
            # substitute commas(,) and whitespaces(\s+) in string using regular expression
            # then split the string
            self.summary = re.sub(
                r"\s+|,\s+", ":", info_spec[0].text.replace(",", "").strip()
            ).split(":")
            # set instances
            self.director = "None"
            self.cast_main = info_spec[1].text
            # remove "도움말" in string using regular expression
            self.rate = re.sub(
                r"\s+", " ", info_spec[2].text.replace("도움말", "").strip()
            )

    """ METHODS """
    ## simply return rank of Movie
    def get_rank(self):
        return self.rank

    ## simply return detailed page URL of Movie
    def get_link(self):
        return self.link

    ## return main poster of Movie
    def get_img(self):
        # replace substring and set an instance(.img)
        self.img = self.link.replace("basic.nhn?code", "photoViewPopup.nhn?movieCode")
        return self.img

    ## update, set instanes(.title, .title_eng) and return titles of Movie
    ## depends on ._get_soup()
    def get_title(self):
        soup = self._get_soup()
        # break(return None) if soup is None : login required on website
        if soup is None:
            # not updated
            return self.title
        # set instances
        self.title = soup.select_one("div.mv_info > h3.h_movie > a").text
        self.title_eng = soup.select_one("div.mv_info > strong.h_movie2").text
        return self.title, self.title_eng

    ## concat plot head and body, then set an instance(.plot) and return plot of Movie
    ## depends on ._get_soup()
    def get_plot(self):
        soup = self._get_soup()
        # break(return None) if soup is None : login required on website
        if soup is None:
            # set an instance as "None" (to write in csv later)
            self.plot = "None"
            return None
        # select plot head and body from soup
        head = soup.select_one("h5.h_tx_story")
        body = soup.select_one("p.con_tx")
        # if head/body is not None, append processed head/body in list(plot)
        plot = [p.text.replace("\xa0", "\n").strip("“") for p in [head, body] if p]
        # concat substrings(list elements) and set an instance(.plot)
        self.plot = "\n\n".join(plot)
        return self.plot

    ## update instance(.point) and return score of Movie rated by netizen
    ## depends on ._get_soup()
    def get_point(self):
        soup = self._get_soup()
        # break(return None) if soup is None : login required on website
        if soup is None:
            # not updated
            return self.point
        # select score rated by netizen from soup
        score = soup.select_one("a#pointNetizenPersentBasic").select("em")
        # concat substrings(list elements) and update the instance(.point)
        self.point = float("".join([i.text for i in score]))
        return self.point

    ## set an instance(.runnigtime) and return running time of Movie
    ## depends on ._get_info_spec(), ._get_soup()
    def get_runningtime(self):
        # break(return None) if soup is None : login required on website
        if self._get_soup() is None:
            # set an instance as "None" (to write in csv later)
            self.runningtime = "None"
            return None
        self._get_info_spec()
        # search a list element include "분" in string
        for info in self.summary:
            if "분" in info:
                # set an instance
                self.runningtime = info
        return self.runningtime

    ## set instances(.release, .release_list) and return release date list of Movie
    ## depends on ._get_info_spec(), ._get_soup()
    def get_release_list(self):
        # break(return None) if soup is None : login required on website
        if self._get_soup() is None:
            # set instance as "None" list (to write in csv later)
            self.release_list = ["None"]
            return None
        self._get_info_spec()
        self.release_list = []
        # find the index of element where the first "개봉" appears
        for index, info in zip(range(len(self.summary)), self.summary):
            if "개봉" in info:
                # if found, break(end loop)
                break
        # find all release dates and save to list
        while index < len(self.summary):
            # the last written release date in (.summary) is original release date
            self.release = "".join(self.summary[index - 2 : index + 1])
            self.release_list.append(self.release)
            # delete release dates from (.summary)
            # index remains the same, length of (.summary) shrinks (makes loop end condition)
            del self.summary[index - 2 : index + 1]
        return self.release_list

    ## simply return director of Movie
    ## depends on ._get_info_spec(), ._get_soup()
    def get_director(self):
        self._get_info_spec()
        return self.director

    ## simply return cast list of Movie
    ## depends on ._get_info_spec(), ._get_soup()
    def get_cast(self):
        self._get_info_spec()
        return self.cast_main

    ## simply return rate of Movie
    ## depends on ._get_info_spec(), ._get_soup()
    def get_rate(self):
        self._get_info_spec()
        return self.rate

    ## set an instance(.category) and return categorical tags of Movie
    ## depends on .get_runningtime(), .get_release_list(), ._get_info_spec(), ._get_soup()
    def get_category(self):
        # break(return None) if soup is None : login required on website
        if self._get_soup() is None:
            # set instance as "None" list (to write in csv later)
            self.category = ["None"]
            return None
        self.get_runningtime()
        self.get_release_list()
        # delete running time from (.summary)
        self.summary.remove(self.runningtime)
        # set an instanse
        self.category = self.summary
        return self.category

    ## set all instance of Movie at once
    ## depends on .get_...() , ._get_...()
    def get_all(self):
        self.get_img()
        self.get_title()
        self.get_plot()
        self.get_point()
        # .get_category() include .get_runningtime, .get_release_list
        # .get_runningtime, .get_release_list include ._get_info_spec
        # with .get_category(), get instances below
        # (.runningtime, .release, .release_list, .director, .cast_main, .rate, .category)
        self.get_category()

    ## print all instance of Movie on console
    ## depends on .get_all()
    def print_all(self):
        self.get_all()
        # if soup is None : login required on website
        # print all instance line by line
        if self._get_soup() is None:
            print(
                "Rank: ",
                self.rank,
                "\nTitle: ",
                self.title,
                "\nURL: ",
                self.link,
                "\nPoint: ",
                self.point,
                "\nPoster: ",
                self.img,
            )
            self._get_soup()
        # print all instance line by line
        else:
            print(
                "Rank: ",
                self.rank,
                "\nTitle: ",
                self.title,
                "\nURL: ",
                self.link,
                "\nPoint: ",
                self.point,
                "\nPoster: ",
                self.img,
                "\nRunning Time: ",
                self.runningtime,
                "\nRate: ",
                self.rate,
                "\nRelease: ",
                self.release,
                "\nPlot: ",
                self.plot,
                "\nDirector: ",
                self.director,
                "\nCast: ",
                self.cast_main,
                "\nCategory: ",
                self.category,
            )

    ## save all instance of Movie on txt file
    ## depends on .get_all()
    def save_all(self):
        self.get_all()
        file = open(f"{self.title}.txt", "w")
        # if soup is None : login required on website
        # save all instance line by line on txt file
        if self._get_soup() is None:
            file.writelines(
                [
                    "Rank: ",
                    str(self.rank),
                    "\nTitle: ",
                    self.title,
                    "\nURL: ",
                    f"Login required: {self.link}",
                    "\nPoint: ",
                    str(self.point),
                    "\nPoster: ",
                    self.img,
                ]
            )
        # save all instance line by line on txt file
        else:
            file.writelines(
                [
                    "Rank: ",
                    str(self.rank),
                    "\nTitle: ",
                    self.title,
                    "\nURL: ",
                    self.link,
                    "\nPoint: ",
                    str(self.point),
                    "\nPoster: ",
                    self.img,
                    "\nRunning Time: ",
                    self.runningtime,
                    "\nRate: ",
                    self.rate,
                    "\nRelease: ",
                    self.release,
                    "\nPlot: ",
                    self.plot,
                    "\nDirector: ",
                    self.director,
                    "\nCast: ",
                    self.cast_main,
                    "\nCategory: ",
                    ", ".join(self.category),
                ]
            )
        file.close()
        ## notify the file is saved
        return print(f"{self.title}.txt file is saved..")


# %% define functions
## get movie contents from ranking site page
def _get_movies(soup, movie_list, page=0):
    # select titles(list), links(list), points(list)  from soup
    titles = soup.select("div.tit5")
    links = soup.select("div.tit5 > a")
    points = soup.select("td.point")
    # iterate titles, links, points at the same time using zip()
    for i, title, link, point in zip(range(len(titles)), titles, links, points):
        # each page contains 50 rankings
        rank = page * 50 + i + 1
        title = title.text.strip()
        # concat main URL and detailed URL as full link
        full_link = "https://movie.naver.com" + link["href"]
        point = float(point.text)
        # initialize Movie class and update instances
        movie = Movie()
        movie.rank = rank
        movie.title = title
        movie.link = full_link
        movie.point = point
        # append Movie object to movie_list(list)
        movie_list.append(movie)


## all movie ranking page (it ranks up to 2000)
## defalut parameter of argument(page) is 2 (i.e. crawl to the top 100)
def rank_all_movies(pages=2):
    if pages > 40 or pages < 1:
        return print("The argument must be between 1 and 40")
    movie_list = []
    # repeat every page
    for page in range(pages):
        # request html of ranking page
        html_pnt = requests.get(URL + f"sel=pnt&page={page+1}")
        # parse html
        soup_pnt = BeautifulSoup(html_pnt.text, "html.parser")
        # get movie contents from parsed html and return movie_list
        _get_movies(soup_pnt, movie_list, page)
        # notify the number of crawled pages
        print(f"rank-chart page{page+1} : rank {page*50+1}-{page*50+50} is crawled..")
    # select date value from soup
    date = soup_pnt.select_one("p.r_date").text.strip()
    # insert date value into movie_list[0], so the index becomes the rank
    # i.e. movie_list[0]=date, movie_list[#]= (...rank # Movie object...) ...
    movie_list.insert(0, date)
    return movie_list


## current movie ranking page (it ranks up to 50)
def rank_cur_movies():
    movie_list = []
    # request html of ranking page
    html_cur = requests.get(URL + "sel=cur")
    # parse html
    soup_cur = BeautifulSoup(html_cur.text, "html.parser")
    # get movie contents from parsed html and return movie_list
    _get_movies(soup_cur, movie_list)
    # select date value from soup
    date = soup_cur.select_one("p.r_date").text.strip()
    # insert date value into movie_list[0], so the index becomes the rank
    # i.e. movie_list[0]=date, movie_list[#]= (...rank # Movie object...) ...
    movie_list.insert(0, date)
    return movie_list


## save movie_list as csv file with file name(filename) and decide which rank(end) to save
## If you don't enter any parameters, the function is run and saved by default for easy use
def save_list(movie_list, end=None, filename=None):
    # when (end) is not entered, use the length of movie_list as default (end)
    if end == None:
        end = len(movie_list)
    # extract date value from movie_list
    date = movie_list[0]
    # slice only Movie objects into movie_list
    movie_list = movie_list[1 : end + 1]
    if movie_list == []:
        return print("Movie list is empty\n")
    # when (filename) is not entered, use "movie_list" as default (filename)
    if filename == None:
        filename = "movie_list"
        # alert that it can be overwritten, because of the same default file name
        print(f"overwrite with {date}_{filename}.csv")
    # start writing files
    # encoded with euc-kr to avoid mojibake
    file = open(f"{date}_{filename}.csv", mode="w", encoding="euc-kr")
    # set csv writer
    writer = csv.writer(file)
    # write the first row (file info)
    writer.writerow(
        [
            "Naver Movie Rank Chart",
            "Crawled Date",
            date,
            "Developped by Jun-Hyeok Park",
            "jun.hyeok@kakao.com",
        ]
    )
    # write the second row (header)
    writer.writerow(
        [
            "Rank",
            "Title",
            "URL",
            "Point",
            "Poster",
            "Running Time",
            "Rate",
            "Release",
            "Plot",
            "Director",
            "Cast",
            "Category",
        ]
    )
    # write rows iterate movie_list
    for row, movie in zip(range(1, len(movie_list) + 1), movie_list):
        # crawl each in-contents from detailed URL of Movie object
        movie.get_all()
        # write instances on a row
        writer.writerow(
            [
                movie.rank,
                movie.title,
                movie.link,
                movie.point,
                movie.img,
                movie.runningtime,
                movie.rate,
                "\n".join(movie.release_list),
                movie.plot,
                movie.director,
                movie.cast_main,
                "\n".join(movie.category),
            ]
        )
        # 30 scale percent gauge bar
        percent_gauge = int(30 * row / len(movie_list))
        # gauge bar for current process status
        print(
            f"{'■'*percent_gauge+'□'*(30-percent_gauge)}({row}/{len(movie_list)}) saved..\r",
            end="",
        )
    # end writing files
    file.close()
    return print(f"{date}_{filename}.csv file is saved..")


## display the movie information on a specific rank using method (.print_all)
def rank_search(movie_list, rank=None):
    # when (rank) is not entered, receive rank from user
    if rank == None:
        rank = int(input("Enter rank:"))
    if rank > len(movie_list) or rank < 1:
        return print("Invalid scope")
    movie_list[rank].print_all()


## save the movie information on a specific rank as a file using method (.save_all)
def rank_save(movie_list, rank=None):
    # when (rank) is not entered, receive rank from user
    if rank == None:
        rank = int(input("Enter rank:"))
    if rank > len(movie_list) or rank < 1:
        return print("Invalid scope")
    movie_list[rank].save_all()


# %%
if __name__ == "__main__":
    """default run"""
    ## rank_all_movies() - save_list()
    all_time_list = rank_all_movies(5)  # 5 pages crawled
    save_list(all_time_list, end=100, filename="all_time_list")  # top 100 movie list

    ## rank_save()
    rank_save(all_time_list, rank=18)  # save 18th ranked Movie from all_time_list

    ## rank_cur_movies() - save_list()
    on_time_list = rank_cur_movies()  # only 1 page crawled
    save_list(on_time_list, end=20, filename="on_time_list")  # top 20 movie list

    ## rank_search()
    rank_search(on_time_list, rank=2)  # print 2nd ranked Movie from all_time_list

    """custom crawling 
    print("==custom crawling==")

    ## rank_all_movies() - save_list()
    print("save all movie ranking list")
    pages = int(input("Enter pages: "))
    all_time_list = rank_all_movies(pages)
    end = input("Enter which rank to end: ")
    filename = input("Enter filename: ")
    save_list(all_time_list, end, filename)

    ## rank_save()
    print("save a specific ranked movie info")
    rank = int(input("Enter rank: "))
    rank_save(all_time_list, rank)

    ## rank_cur_movies() - save_list()
    print("save current movie ranking list")
    on_time_list = rank_cur_movies()
    end = input("Enter which rank to end: ")
    filename = input("Enter filename: ")
    save_list(on_time_list, end, filename)

    ## rank_search()
    print("print a specific ranked movie info")
    rank = int(input("Enter rank: "))
    rank_search(on_time_list, rank)
    """

