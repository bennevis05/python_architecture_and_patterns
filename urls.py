import views

urls = {
    '/': views.main_view,
    '/categories/': views.categories_view,
    '/courses/': views.courses_view,
    '/contact/': views.contact_view,
    '/manage/': views.manage_page_view,
    '/add_category/': views.add_category_view,
    '/add_course/': views.add_course_view,
}
