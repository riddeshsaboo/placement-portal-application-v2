<template>
    <div>
        <h1>Company Registration</h1>
    <input
        v-model="email"
        type="email"
        placeholder="Company Email"
    />
    <br><br>
    <input
        v-model="password"
        type="password"
        placeholder="Password"
    />
    <br><br>
    <input
        v-model="company_name"
        type="text"
        placeholder="Company Name"
    />
    <br><br>
    <input
        v-model="industry"
        type="text"
        placeholder="Industry"
    />
    <br><br>
    <input
        v-model="location"
        type="text"
        placeholder="Location"
    />
    <br><br>
    <input
        v-model="website"
        type="text"
        placeholder="Website (Optional)"
    />
    <br><br>
    <textarea
        v-model="description"
        placeholder="Company Description (Optional)"
        rows="5"
        cols="40"
    ></textarea>
    <br><br>
    <button @click="registerCompany">
        Register Company
    </button>
    <br><br>
    <h4>
        Already have an account?
        <router-link to="/">Login</router-link>
    </h4>
    <h4>
        Student Registration?
        <router-link to="/register/student">
            Register as Student
        </router-link>
    </h4>
</div>
</template>
<script>
import axios from "axios"
export default {
    data() {
        return {
            email: "",
            password: "",
            company_name: "",
            industry: "",
            location: "",
            website: "",
            description: ""
        }
    },
    methods: {
        async registerCompany() {
            try {
                const response = await axios.post(
                    "http://127.0.0.1:5000/register/company",
                    {
                        email: this.email,
                        password: this.password,
                        company_name: this.company_name,
                        industry: this.industry,
                        location: this.location,
                        website: this.website,
                        description: this.description
                    }
                )
                alert(response.data.message)
                this.$router.push("/")
            } catch (error) {
                alert(error.response.data.message)
            }
        }
    }
}
</script>