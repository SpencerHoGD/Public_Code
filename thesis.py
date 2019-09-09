import pandas
import re
import matplotlib.pyplot as plt


def format_text(string):
    string = string.lower()
    p = re.compile('\W')
    string = re.sub(p, ' ', string)
    return string


def create_item(string):
    first_person = ['i', 'we', 'me', 'my', 'us', 'our', 'mine', 'ours']
    third_person = ['they', 'them', 'their', 'students', 'student']

    word_list = [word for word in string.split(' ') if word]
    token = len(word_list)

    word_count = dict()
    for each in word_list:
        if each:
            word_count[each] = word_count.get(each, 0) + 1

    item = {
        "token": [token]
    }

    # 输入第一人称的量
    for each_word in first_person:
        item[each_word] = [word_count.get(each_word, 0)]

    # 输入第三人称的量
    for each_word in third_person:
        item[each_word] = [word_count.get(each_word, 0)]

    # 第一人称总和
    item['first_person'] = [sum([word_count.get(word, 0) for word in first_person])]

    # 第三人称总和
    item['third_person'] = [sum([word_count.get(word, 0) for word in third_person])]

    return pandas.DataFrame(item)


def main():
    article1 = '''
There's no way I could have held down a part-time job as an undergraduate. With relatively short eight-week terms, at least three essays constantly on the go, and a never-ending reading list, on top of the extra-curricular commitments so crucial for one's CV, I would have burned out.
When sleep is considered a luxury and there's never a day when you couldn't be working, faking a smile behind a supermarket counter is the last thing you want to be doing.
It's often said at Cambridge that students have to sacrifice one of three aspects of their lives to survive: work, sleep or their social life. I found this to be true. Sometimes even maintaining good quality in one of these areas was a challenge.
Oxbridge students are advised against undertaking part-time work and, I believe it's for good reason. A Cambridge University spokesperson says this is because "terms are short and intense".
You may wonder what the difference is between part-time jobs and the hours many students spend involved in sport, arts or student media during term. The Cambridge spokesperson says "these activities are part of the student experience" so the university has a duty to encourage students to participate in them.
Andy Jefferies, from the senior tutors committee at Cambridge, says there isn't necessarily a difference between such commitments and part-time work. He says: "We try to discourage students from doing part-time work if they're struggling to keep up and meet deadlines.
"Obviously extracurricular activities can be overdone to the extent that they interfere with academic work, but they're fine if they're balanced with it."
Universities like Oxford and Cambridge provide generous bursaries. They prevent students from being forced into jobs that would compromise their academic achievement, which is, after all, the main point of university.
It is true though that university is expensive, so students might feel the need to take on part-time work to meet living costs. I was lucky enough to qualify for a bursary and would have struggled to maintain a decent quality of life without it.
Bursaries might not be enough to sustain some students, so there is always the option of a holiday job. With three months off over the summer, many take up paid internships or retail work to tide themselves over for the following academic year.
If you're still struggling financially, there may well be help available. Jeffries says: "Don't suffer in silence or feel forced to go and work. Talk to the college first and you may be surprised about how generous it can be, but it depends on the circumstances."
'''

    article2 = '''
While the argument that university years are for studying is a valid one, it is not the whole picture. For myself and many other students, there are lots of reasons for taking on part-time work.
Financial issues is perhaps the most pressing reason to work, but a part-time job is also an opportunity to gain experience in your chosen field, put study into practice, gain relevant skills and make networks that will help you get a job after uni.
With university fees currently at £9000 and hefty living costs on top, life as a student is expensive I need to work.
I work 18.5 hours each week at The University of Worcester, where I am a student, earning around £375 per month. I use this money to pay for the living costs not covered by my loan.
Some people argue that part-time work can have a negative impact on your studies, but I've found that by being organised you can manage both. It helps that my job is at the university where I am studying – they are extremely flexible and say that students should always prioritise their studies.
Christina Weaver, working with children and families student, works 17.5 hours per week in a school.
She says: "It is tough finding the right balance but the experience is a fundamental element of my course. Experience is the key that students are using to distinguish themselves from other applicants."
Most employers ask for experience alongside a degree, and working while at uni puts you in a much better position when it comes to finding a graduate job.
Emily Coppen, a first-year marketing, advertising and PR students works at Waitrose. She argues that working "allows you to practice for the 'real world' where you may have numerous commitments".
What is the point of studying a subject just in theory? After all, will you not be putting theory into practice after university with a job? Part-time work is a good way for students to develop practical skills.
Alina Tatar, a third-year illustration student, works 15-20 hours every week. She says: "Working allows me to develop skills for future employment."
For students, part-time employment is a good way to make relationships in the workplace that you might not have the chance to develop otherwise.
Olivia Bullough, a first-year business information technology student says: "Part-time employment is a good way to make contacts to secure full-time employment upon graduation"
Why else do you go to university? Personally, I went to uni to improve my chance of getting a job.
'''

    df = pandas.DataFrame()
    articles = [article1, article2]

    for article in articles:
        article1 = format_text(article)
        item = create_item(article1)
        df = pandas.concat([df, item], ignore_index=True)

    df['first_percent'] = df['first_person'] / df['token'] * 100
    df['third_percent'] = df['third_person'] / df['token'] * 100
    print(df)

    plt.plot(df.token, df.first_percent)
    plt.ylabel('percent')
    plt.xlabel('token')

    plt.plot(df.token, df.third_percent)
    plt.ylabel('percent')
    plt.xlabel('token')

    plt.show()

    # print(article.split(' '))


if __name__ == '__main__':
    main()