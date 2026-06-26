<template>
    <div v-if="role == 'student' ">
        <h1>Welcome Student</h1>
        <button @click="logout">Logout</button>
    </div>
    <div v-else>
        <h1>You are not student! Please <router-link to="/login">Login</router-link></h1>
    </div>
</template>

<script>
export default {
    data(){
        const role = localStorage.getItem("role");
        return {
            role : role 
        }
    },

    mounted() {
        if (this.role !== "student") {
            if(this.role == "company"){
                this.$router.push("/company")
            }
            else if(this.role == "admin"){
                this.$router.push("/admin")
            }
            else{
                this.$router.push("/login")
            }
        }

    },

    methods : {
        logout() {
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/login");
        }
    }

}
</script>