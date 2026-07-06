import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterStudentView from '../views/RegisterStudentView.vue'
import RegisterCompanyView from '../views/RegisterCompanyView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import AddJobPosting from '../views/AddJobPosting.vue'
import ManageJobPosting from "../views/ManageJobPosting.vue"
import StudentJobPosting from "../views/StudentJobPosting.vue"
import ReviewApplication from "../views/ReviewApplication.vue"
import ReviewApplicationStudent from "../views/ReviewApplicationStudent.vue"
import StudentProfile from '../views/StudentProfile.vue'
import AdminStudentProfile from '../views/AdminStudentProfile.vue'
import AdminCompanyProfile from '../views/AdminCompanyProfile.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: HomeView
        },
        {
            path: '/login',
            component: LoginView
        },
        {
            path: '/register/student',
            component: RegisterStudentView
        },
        {
            path: '/register/company',
            component: RegisterCompanyView
        },
        {
            path: '/admin',
            component: AdminDashboard
        },
        {
            path: '/student',
            component: StudentDashboard
        },
        {
            path: '/company',
            component: CompanyDashboard
        },
        {
            path: '/company/add_job_posting',
            component: AddJobPosting
        },
        {
            path: "/company/job_posting/:id",
            component: ManageJobPosting
        },
        {
            path:"/student/job_posting/:id",
            component:StudentJobPosting
        },
        {
            path: "/company/application/:id",
            component: ReviewApplication
        },
        {
            path: "/student/application/:id",
            component: ReviewApplicationStudent
        },
        {
            path: "/student/profile",
            component: StudentProfile
        },
        {
            path: "/admin/student/:id",
            component: AdminStudentProfile
        },
        {
            path: "/admin/company/:id",
            component: AdminCompanyProfile
        }
    ]
})

export default router