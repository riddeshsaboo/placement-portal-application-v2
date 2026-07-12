<template>

<div>
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
          <router-link to="/student" class="text-decoration-none text-dark fs-3 fw-bold">Student Dashboard</router-link>
      </div>
    </nav> 
    <router-link to="/student" class="btn btn-outline-secondary m-3">← Back</router-link>
    
    <h2 class="mx-3">{{ job.title }}</h2>
    <div class="card m-3 border border-dark">
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
            <hr>
            <div v-if="!job.already_applied">
                <h5>ATS Resume Screening</h5>
                <p class="mb-1">
                    <strong>Resume Match Score :</strong> {{ resume_match_score }}%
                </p>
                <p>
                <span v-if="recommendation == 'Excellent Match'" class="badge bg-success">Recommendation: {{ recommendation }}</span>
                <span v-else-if="recommendation == 'Good Match'" class="badge bg-warning">Recommendation: {{ recommendation }}</span>
                <span v-else class="badge bg-danger">{{ recommendation }}</span>
                </p>

                <div class="row">
                    <div class="col-md-6" v-if="matched_skills.length > 0">
                        <h6 class="text-success">Matched Skills</h6>
                        <ul>
                            <li v-for="skill in matched_skills" :key="skill">{{ skill }}</li>
                        </ul>
                    </div>
                    <div class="col-md-6" v-else>
                        <h6 class="text-warning">No Matched Skills</h6>
                    </div>

                    <div class="col-md-6" v-if="missing_skills.length > 0">
                        <h6 class="text-danger">Missing Skills</h6>
                        <ul>
                            <li v-for="skill in missing_skills" :key="skill">{{ skill }}</li>
                        </ul>
                    </div>
                    <div class="col-md-6" v-else>
                        <h6 class="text-warning">No Missing Skills</h6>
                    </div>

                </div>
                <div class="alert alert-info border border-dark">It is advised to improve your resume by adding the missing skills if any before applying</div>
            </div>
            
            <button class="btn btn-info m-1" v-if="job.already_applied" disabled>Already applied on {{ formatDate(job.applied_at )}}</button>
            <button class="btn btn-success m-1" v-else @click="applyJob">Apply</button>
            <router-link :to="`/student/application/${job.application_id}`" class="btn btn-success my-2 m-1" v-if="job.already_applied">View Application</router-link> 
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
            resume_match_score:0,
            recommendation:"",
            matched_skills:[],
            missing_skills:[]
        }
    },
    async mounted(){
        await this.loadJob()
        await this.loadResumeMatch()
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
            if(!date) {
                return "NA";
            }
            return new Date(date.replace(" GMT","")).toLocaleString("en-GB")
        },

        async loadResumeMatch(){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/student/resume_screener/${this.$route.params.id}`,
                    {headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}}
                )

                this.resume_match_score=response.data.resume_score
                this.recommendation=response.data.recommendation
                this.matched_skills=response.data.matched_skills
                this.missing_skills=response.data.missing_skills

            }catch(e){
                console.log(e);
            }
        },
    }

}

</script>