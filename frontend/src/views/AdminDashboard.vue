<template>
    <div v-if="role == 'admin' ">
        <h1>Welcome Admin</h1>
        <button @click="logout">Logout</button>
    </div>
    <div v-else>
        <h1>You are not admin! Please <router-link to="/">Login</router-link></h1>
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
        if (this.role !== "admin") {
            if(this.role == "student"){
                this.$router.push("/student")
            }
            else if(this.role == "company"){
                this.$router.push("/company")
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