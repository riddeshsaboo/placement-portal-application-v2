<template>
    <div>
        <h1>Student Registration</h1>
    <input v-model="email" type="email" placeholder="Email" />
    <br><br>
    <input v-model="password" type="password" placeholder="Password" />
    <br><br>
    <input v-model="full_name" type="text" placeholder="Full Name" />
    <br><br>
    <input v-model="cgpa" type="number" step="0.01" placeholder="CGPA" />
    <br><br>
    <input v-model="education" type="text" placeholder="Education" />
    <br><br>
    <h4>Branch</h4>
    <label>
        <input v-model="branch" type="radio" value="Computer Science" />
        Computer Science
    </label>

    <label>
        <input v-model="branch" type="radio" value="Electrical" />
        Electrical
    </label>

    <label>
        <input v-model="branch" type="radio" value="Electronics" />
        Electronics
    </label>

    <label>
        <input v-model="branch" type="radio" value="Mechanical" />
        Mechanical
    </label>

    <label>
        <input v-model="branch" type="radio" value="Other" />
        Other
    </label>

    <div v-if="branch === 'Other'">
        <br>
        <input
            v-model="customBranch"
            type="text"
            placeholder="Enter your branch"
        />
    </div>
    <br><br>
    <input v-model="contact" type="text" placeholder="Contact" />
    <br><br>
    <input v-model="skills" type="text" placeholder="Skills" />
    <br><br>
    <input v-model="experience" type="text" placeholder="Experience" />
    <br><br>
    <button @click="registerStudent">
        Register
    </button>
    <br><br>
    <h4>
        Already have an account?
        <router-link to="/">Login</router-link>
    </h4>
    <h4>
        Company Registration?
        <router-link to="/register/company">Register</router-link>
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
            full_name: "",
            cgpa: "",
            education: "",
            branch: "",
            customBranch: "",
            contact: "",
            skills: "",
            experience: ""
        }
    },
    methods: {
        async registerStudent() {
            try {
                const finalBranch =
                    this.customBranch.trim() || this.branch
                const response = await axios.post(
                    "http://127.0.0.1:5000/register/student",
                    {
                        email: this.email,
                        password: this.password,
                        full_name: this.full_name,
                        cgpa: this.cgpa,
                        education: this.education,
                        branch: finalBranch,
                        contact: this.contact,
                        skills: this.skills,
                        experience: this.experience
                    }
                )
                alert(response.data.message)
                this.$router.push("/")

            } catch (error) {
                alert(error.response.data.message || "Something went wrong")
            }
        }
    }
}
</script>