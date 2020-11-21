from datacenter.models import Schoolkid, Chastisement, Commendation, Lesson, Mark


def get_schoolkid(schoolkid: str):
    try:
        Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.MultipleObjectsReturned:
        print('Скрипт нашел больше 1го ученика с похожим именем. Попробуйте указать имя и фамилию.')
        return
    except Schoolkid.DoesNotExist:
        print('Имя указано не верно либо ученика с таким именем/фамилией не существует')
        return
    return Schoolkid.objects.get(full_name__contains=schoolkid)


def fix_marks(schoolkid: str):
    child = get_schoolkid(schoolkid)
    Mark.objects.filter(schoolkid=child, points__in=[2, 3]).update(points=5)
    print('Выполнено')


def remove_chastisements(schoolkid: str):
    child = get_schoolkid(schoolkid)
    Chastisement.objects.filter(schoolkid=child).delete()
    print('Выполнено')


def create_commendation(schoolkid: str, subject: str):
    child = get_schoolkid(schoolkid)
    lessons = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject).order_by('?')
    chosen_lesson = lessons[0]
    commendation_texts = ['Молодец', 'Гораздо лучше, чем я ожидал!', 'Сказано здорово – просто и ясно!',
                          'Ты сегодня прыгнул выше головы!', 'Я тобой горжусь']
    commendation_number = randint(0, len(commendation_texts))
    chosen_text = commendation_texts[commendation_number]
    Commendation.objects.create(text=chosen_text, created=chosen_lesson.date, subject=chosen_lesson.subject,
                                schoolkid=child, teacher=chosen_lesson.teacher)
    print('Выполнено')


def do_all(schoolkid: str, subject: str):
    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, subject)
    print(f'Карма ученка {schoolkid} очищена')