<template>
    <div>
        <h1>Login</h1>
        <input v-model="email" type="email" placeholder="Email">
        <br><br>
        <input v-model="password" type="password" placeholder="Password"/>
        <br><br>
        <button @click="login">Login</button>
        <br><br>
        <h4>New student? <router-link to="/register/student">Register</router-link></h4>
        <h4>New company? <router-link to="/register/company">Register</router-link></h4>

    </div>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            email: "",
            password: ""
        }
    },

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
            catch(error){
                alert(error.response.data.message)
            }
        }
    }
}
</script>