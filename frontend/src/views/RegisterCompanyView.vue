<template>
<div>
    <nav class="p-2 bg-body-tertiary">
        <router-link class="navbar-brand" to="/">
            <h3 class="fw-bold">Placement Portal V2</h3>
        </router-link>
    </nav>

    <div class="container d-flex justify-content-center align-items-center mt-2" style="min-height:85vh">
        <div style="width:600px" class="p-3 bg-body-tertiary rounded border border-warning">
            <div class="card-header text-center">
                <h2>Company Registration</h2>
            </div>
            <hr>
            <div class="card-body">
                <label class="form-label">Company Email</label>
                <input class="form-control mb-1" v-model="email" type="email" placeholder="Company Email" />
                <label class="form-label">Password</label>
                <input class="form-control mb-1" v-model="password" type="password" placeholder="Password" />
                <label class="form-label">Company Name</label>
                <input class="form-control mb-1" v-model="company_name" type="text" placeholder="Company Name" />
                <label class="form-label">Industry</label>
                <input class="form-control mb-1" v-model="industry" type="text" placeholder="Industry" />
                <label class="form-label">Location</label>
                <input class="form-control mb-1" v-model="location" type="text" placeholder="Location" />
                <label class="form-label">Website (Optional)</label>
                <input class="form-control mb-1" v-model="website" type="text" placeholder="Website (Optional)" />
                <label class="form-label">Company Description (Optional)</label>
                <textarea class="form-control mb-2" v-model="description" placeholder="Company Description" rows="5"></textarea>
               
                <button @click="registerCompany" class="btn btn-warning w-100 mt-3 mb-3">Register Company</button>
                <hr>
                
                <p class="text-center mb-2">
                    Already have an account?
                    <router-link to="/login">Login</router-link>
                </p>
                <p class="text-center mb-2">
                    Student Registration?
                    <router-link to="/register/student">Register as Student</router-link>
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
                const emailRegex=/^[^\s@]+@[^\s@]+\.[^\s@]+$/
                if(!emailRegex.test(this.email)){
                    alert("Please enter a valid email")
                    return
                }
                const passwordRegex=/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/
                if(!passwordRegex.test(this.password)){
                    alert("Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character")
                    return
                }
                if(this.website.length != 0){
                    if(!this.isUrlSyntaxValid(this.website)){
                        alert("Invalid Website URL format");
                        return ;
                    }
                }
                if(this.description.length>1000){
                    alert("Company description cannot exceed 1000 characters")
                    return
                }
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
                this.$router.push("/login")
            } catch (error) {
                alert(error.response.data.message)
            }
        },

        isUrlSyntaxValid(string) {
            return URL.canParse(string);
        },
    }
}
</script>