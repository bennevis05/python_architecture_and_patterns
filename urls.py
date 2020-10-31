import views

urls = {
    '/': views.main_view,
    '/categories/': views.categories_view,
    '/courses/': views.courses_view,
    '/contact/': views.contact_view,
    '/manage/': views.manage_page_view,
    '/add_category/': views.add_category_view,
    '/add_course/': views.add_course_view,
    '/add_user/': views.add_user_view,
    '/change_course/': views.change_course,
    '/change_course_confirm/': views.change_course_confirm,

    # API
    '/api_get_courses/': views.api_get_courses
}
