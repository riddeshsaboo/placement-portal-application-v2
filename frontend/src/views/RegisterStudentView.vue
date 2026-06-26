<template>
<div>
    <nav class="p-2 bg-body-tertiary">
        <router-link class="navbar-brand" to="/">
            <h3 class="fw-bold">Placement Portal V2</h3>
        </router-link>
    </nav>

    <div class="container d-flex justify-content-center align-items-center mt-2" style="min-height:85vh">
        <div style="width:600px" class="p-3 bg-body-tertiary rounded border border-success">
            <div class="card-header text-center">
                <h2>Student Registration</h2>
            </div>
            <hr>
            <div class="card-body">
                <label class="form-label">Email</label>
                <input class="form-control mb-1" v-model="email" type="email" placeholder="Email" />
                <label class="form-label">Password</label>
                <input class="form-control mb-1" v-model="password" type="password" placeholder="Password" />
                <label class="form-label">Full Name</label>
                <input class="form-control mb-1" v-model="full_name" type="text" placeholder="Full Name" />
                <label class="form-label">CGPA</label>
                <input class="form-control mb-1" v-model="cgpa" type="number" step="0.01" placeholder="CGPA" />
                <label class="form-label">Education</label>
                <input class="form-control mb-1" v-model="education" type="text" placeholder="Education" />
                <label class="form-label">Branch</label>
                <br>
                <label class="form-label m-1">
                    <input v-model="branch" type="radio" value="Computer Science" />
                    Computer Science
                </label>

                <label class="form-label m-1">
                    <input v-model="branch" type="radio" value="Electrical" />
                    Electrical
                </label>

                <label class="form-label m-1">
                    <input v-model="branch" type="radio" value="Electronics" />
                    Electronics
                </label>

                <label class="form-label m-1">
                    <input v-model="branch" type="radio" value="Mechanical" />
                    Mechanical
                </label>

                <label class="form-label m-1">
                    <input v-model="branch" type="radio" value="Other" />
                    Other
                </label>

                <div v-if="branch === 'Other'">
                    <br>
                    <input class="form-control"
                        v-model="customBranch"
                        type="text"
                        placeholder="Enter your branch"
                    />
                </div>
                <label class="form-label">Contact</label>
                <input class="form-control mb-1" v-model="contact" type="text" placeholder="Contact" />
                <label class="form-label">Skills</label>
                <input class="form-control mb-1" v-model="skills" type="text" placeholder="Skills" />
                <label class="form-label">Experience</label>
                <input class="form-control mb-2" v-model="experience" type="text" placeholder="Experience" />
               
                <button @click="registerStudent" class="btn btn-success w-100 mt-3 mb-3">Register</button>
                <hr>
                <p class="text-center mb-2">
                    Already have an account?
                    <router-link to="/login">Login</router-link>
                </p>
                <p class="text-center mb-2">
                    Company Registration?
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
                this.$router.push("/login")

            } catch (error) {
                alert(error.response.data.message || "Something went wrong")
            }
        }
    }
}
</script>