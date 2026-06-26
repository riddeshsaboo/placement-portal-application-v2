<template>
<div>
    <nav class="p-2 bg-body-tertiary">
        <router-link class="navbar-brand" to="/">
            <h3 class="fw-bold">Placement Portal V2</h3>
        </router-link>
    </nav>
    <div class="container">
        <div class="row justify-content-center text-center mt-5">
            <div class="col-lg-8">
                <h1 class="display-4 fw-bold">
                    Placement Portal V2
                </h1>
                <p class="lead mt-3">
                    A centralized platform to manage campus placements, companies, students and recruitment drives efficiently.
                </p>
                <div class="mt-4" v-if="!isLoggedIn">
                    <router-link to="/login" class="btn btn-outline-primary btn-lg m-2">Login</router-link>
                    <router-link to="/register/student" class="btn btn-outline-success btn-lg m-2">Register as Student</router-link>
                    <router-link to="/register/company" class="btn btn-outline-warning btn-lg m-2">Register as Company</router-link>
                </div>
                <div v-else>
                    <router-link to="/login" class="btn btn-outline-primary btn-lg m-2">Dashboard</router-link>
                </div>
            </div>
        </div>
        
    </div>
</div>
</template>

<script>
export default {
    data(){
        return {
            isLoggedIn: false,
            loginRole: null,
        }
    },
    mounted(){
        this.checkLoggedIn()
    },

    methods: {
        checkLoggedIn(){
            let role = localStorage.getItem("role")

            if(role == "admin"){
                this.isLoggedIn = true
                this.loginRole = "admin"
            }
            else if(role == "company"){
                this.isLoggedIn = true
                this.loginRole = "company"
            }
            else if(role == "student"){
                this.isLoggedIn = true
                this.loginRole = "student"
            }
            else{
                this.isLoggedIn = false
                this.loginRole = null
            }
        }
    }
}
</script>