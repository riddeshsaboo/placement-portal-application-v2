import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegisterStudentView from '../views/RegisterStudentView.vue'
import RegisterCompanyView from '../views/RegisterCompanyView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
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
        }
    ]
})

export default router