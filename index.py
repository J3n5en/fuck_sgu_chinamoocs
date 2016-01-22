# coding:utf-8
import requests, re
from mooc_login import get_cookie
from pyquery import PyQuery as pq
username = "username"
password = "password"
cookie = get_cookie(username, password) # 从mooc_login取回来cookies
s = requests.Session()
def get_course_id():
        course_ids = []
        postdata= {
            "tabIndex": 1,
            "searchType": 0,
            "schoolcourseType": 0,
            "pageIndex": 1
        }
        course_page = s.post("http://sgu.chinamoocs.com/portal/ajaxMyCourseIndex.mooc", data=postdata, cookies=cookie).text
        # 　取ajax回来的课程列表　，下一行是解析
        course_page_pqed = pq(course_page)
        links = course_page_pqed(".view-shadow")
        # 在解析的页面里寻找.view-shadow（就是去学习按钮）
        for link in links:
            course_ids.append(re.split("index/|\.mooc", link.get("href"))[1])
            # 取课程ＩＤ
        print 'course_ids', course_ids
        return course_ids


def get_course_info(course_id):
        info_page = pq(s.get("http://sgu.chinamoocs.com/portal/session/unitNavigation/"+course_id+".mooc", cookies=cookie).text)
        cells = info_page(".lecture-title")
        # 解析课程内容页，并找到每节课的ｄｉｖ
        for cell in cells:　　#　这里是取没上的课的item(去掉上完的，去掉习题．)
            cell_ele = pq(cell)
            # unitid_ele = cell_ele(".unitItem")
            if cell_ele(".icon-play-done") != [] or cell_ele(".unitItem").text() == u"练一练  章节练习":
                continue
            # unitid = unitid_ele.attr("unitid")
            itemid = cell_ele(".linkPlay").attr("itemid")
            response = s.get("http://sgu.chinamoocs.com/study/updateDurationVideo.mooc?itemId="+itemid+"&isOver=2&duration=700000&currentPosition=700000", cookies=cookie)
            # 发送请求，刷课
            if response.status_code != 200:
                print "GGGG"
if __name__ == '__main__':
    nums = get_course_id()
    for num in nums:
        get_course_info(num)
