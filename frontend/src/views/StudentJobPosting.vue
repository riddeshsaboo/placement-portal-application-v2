<template>

<div class="container mt-4">
    <h2>{{ job.title }}</h2>
    <div class="card mt-3">
        <div class="card-header">Job Details</div>
        <div class="card-body">
            <table class="table">
                <tr>
                    <th width="220">Company</th>
                    <td>{{ job.company_name }}</td>
                </tr>
                <tr>
                    <th>Description</th>
                    <td>{{ job.description || "NA" }}</td>
                </tr>
                <tr>
                    <th>Package(LPA)</th>
                    <td>{{ job.salary || "Not Disclosed" }}</td>
                </tr>
                <tr>
                    <th>Minimum CGPA</th>
                    <td>{{ job.min_cgpa || "Not Required" }}</td>
                </tr>
                <tr>
                    <th>Skills</th>
                    <td>{{ job.skills_required || "NA" }}</td>
                </tr>
                <tr>
                    <th>Location</th>
                    <td>{{ job.job_location || "NA" }}</td>
                </tr>
                <tr>
                    <th>Vacancies</th>
                    <td>{{ job.vacancies }}</td>
                </tr>
                <tr>
                    <th>Deadline</th>
                    <td>{{ formatDate(job.deadline) }}</td>
                </tr>
            </table>
            <button class="btn btn-info" v-if="job.already_applied" disabled>Already applied on {{ formatDate(job.applied_at )}}</button>
            <button class="btn btn-success" v-else @click="applyJob">Apply</button>
            <router-link :to="`/student/application/${job.application_id}`" class="btn btn-success mx-2" v-if="job.already_applied">View Application</router-link> 
        </div>
    </div>
</div>
</template>
<script>
import axios from "axios"
export default{
    data(){
        return{
            job:{},
        }
    },
    async mounted(){
        await this.loadJob()
    },
    methods:{
        async loadJob(){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/student/job_posting/${this.$route.params.id}`,{ headers:{ Authorization:`Bearer ${localStorage.getItem("token")}`} })
                this.job=response.data
            }catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong")
                this.$router.push("/student")
            }
        },

        async applyJob(){
            try{
                const response = await axios.post(`http://127.0.0.1:5000/student/job_posting/${this.job.id}/apply`,{},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                alert(response.data.message)
                await this.loadJob()
            }catch(e){
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

        formatDate(date){
            return new Date(date).toLocaleString("en-GB")
        }
    }

}

</script>