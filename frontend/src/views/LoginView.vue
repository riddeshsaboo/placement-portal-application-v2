<template>
<div>
    <nav class="p-2 bg-body-tertiary">
        <router-link class="navbar-brand" to="/">
            <h3 class="fw-bold">Placement Portal V2</h3>
        </router-link>
    </nav>

    <div class="container d-flex justify-content-center align-items-center" style="min-height:85vh">
        <div style="width:420px" class="p-3 bg-body-tertiary rounded border border-primary">
            <div class="card-header text-center">
                <h2>Login</h2>
            </div>
            <hr>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input v-model="email" type="email" class="form-control" placeholder="Enter Email">
                </div>
                <div class="mb-4">
                    <label class="form-label">Password</label>
                    <input v-model="password" type="password" class="form-control" placeholder="Enter Password">
                </div>
                <button @click="login" class="btn btn-primary w-100">Login</button>
                <hr>
                <p class="text-center mb-2">
                    New Student?
                    <router-link to="/register/student">Register</router-link>
                </p>
                <p class="text-center mb-0">
                    New Company?
                    <router-link to="/register/company">Register</router-link>
                </p>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            email: "",
            password: "",
            isLoggedIn: false,
            loginRole: null,
        }
    },
    async mounted(){
        this.checkLoggedIn()
        if(this.isLoggedIn){
            this.$router.push(`/${this.loginRole}`)

        }
    }
    ,

    methods: {
        async login() {
            try {

                const response = await axios.post(
                    "http://127.0.0.1:5000/login",
                    {
                        email: this.email,
                        password: this.password
                    }
                )

                localStorage.setItem("token",response.data.token)

                localStorage.setItem("role",response.data.role)

                if(response.data.role === "admin"){
                    this.$router.push("/admin")
                }
                else if(response.data.role === "company"){
                    this.$router.push("/company")
                }
                else{
                    this.$router.push("/student")
                }

            }
            catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },

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