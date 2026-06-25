<template>
    <div v-if="role == 'company' ">
        <h1>Welcome Company</h1>
        <button @click="logout">Logout</button>
        <br>
        <br>
        <router-link to="/company/add_job_posting">New Job posting</router-link>
    </div>
    <div v-else>
        <h1>You are not company! Please <router-link to="/">Login</router-link></h1>
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
        if (this.role !== "company") {
            if(this.role == "student"){
                this.$router.push("/student")
            }
            else if(this.role == "admin"){
                this.$router.push("/admin")
            }
            else{
                this.$router.push("/")
            }
        }

    },

    methods : {
        logout() {
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/");
        }
    }

}
</script>