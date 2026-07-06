<template>
    <div>
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
          <router-link to="/admin" class="text-decoration-none text-dark fs-3 fw-bold">Admin Dashboard</router-link>
      </div>
    </nav> 

    <div class="card m-3 border border-dark">
        <div class="card-header">
            <span class="m-2 fw-bold fs-4">Student Details</span>
        </div>
        <div class="card-body">
            <table class="table m-2">
                <tr>
                    <th width="220">Full Name</th>
                    <td>{{ student.full_name }}</td>
                </tr>
                <tr>
                    <th>CGPA</th>
                    <td>{{ student.cgpa }}</td>
                </tr>
                <tr>
                    <th>Branch</th>
                    <td>{{ student.branch  }}</td>
                </tr>
                <tr>
                    <th>Education</th>
                    <td>{{ student.education }}</td>
                </tr>
                <tr>
                    <th>Skills</th>
                    <td>{{ student.skills }}</td>
                </tr>
                <tr>
                    <th>Experience</th>
                    <td>{{ student.experience }}</td>
                </tr>
                <tr>
                    <th>Resume</th>
                    <td>
                        <button v-if="this.student.resume_path != null" @click="downloadResume" class="btn btn-primary bg-primary btn-sm my-2">Download Resume</button>
                        <span v-else class="fw-bold">Not uploaded</span>
                    </td>
                </tr>
                <tr>
                    <th>Contact</th>
                    <td>{{ student.contact }}</td>
                </tr>
                <tr>
                    <th>LinkedIn Url</th>
                    <td>
                        <a v-if="student.linkedin_url" :href="student.linkedin_url" target="_blank">{{ student.linkedin_url }}</a>
                        <span v-else class="fw-bold">Not Provided</span>
                    </td>
                </tr>
                <tr>
                    <th>GitHub Url</th>
                    <td>
                        <a  v-if="student.github_url" :href="student.github_url" target="_blank">{{ student.github_url }}</a>
                        <span v-else class="fw-bold">Not Provided</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div class="card m-3 border border-dark">
        <div v-if="applications.length > 0">
            <div class="card-header">
                <span class="m-2 fw-bold fs-4">Applications</span>
            </div>
            <div class="input-group m-1 mt-3 row">
                <div class="col-md-6">
                    <input type="search" v-model="search_application" placeholder="Search Applications by company name / status" class="form-control border border-dark" />
                </div>
            </div>
                <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
                    <table class="table table-hover">
                        <thead class="table-info">
                            <tr>
                                <th>Sr. No.</th>
                                <th>Company Name</th>
                                <th>Job title</th>
                                <th>Status</th>
                                <th>Applied on</th>
                                <th>Joining Date</th>
                                <th>Offer Letter</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(appl,index) in filteredApplications" :key="appl.id">
                                <td>{{ index+1 }}</td>
                                <td>{{ appl.company_name }}</td>
                                <td>{{ appl.job_title }}</td>
                                <td>
                                    <span class="badge bg-warning text-dark" v-if="appl.status === 'applied'">Applied</span>
                                    <span class="badge bg-primary" v-else-if="appl.status === 'shortlisted'">Shortlisted</span>
                                    <span class="badge bg-primary-subtle" v-else-if="appl.status === 'interview_scheduled'">Interview Scheduled</span>
                                    <span class="badge bg-success" v-else-if="appl.status === 'selected'">Selected</span>
                                    <span class="badge bg-success" v-else-if="appl.status === 'placed'">Placed</span>
                                    <span class="badge bg-danger" v-else>Rejected</span>
                                </td>
                                <td>{{ formatDate(appl.applied_at) }}</td>
                                <td v-if="appl.joining_date">{{ formatDate(appl.joining_date) }}</td>
                                <td v-else>NA</td>
                                <td v-if="appl.offer_letter">
                                    <button @click="download_offer_letter(appl.id)" class="btn btn-info btn-sm">View offer letter</button>
                                </td>
                                <td v-else>NA</td>
                            </tr>
                        </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <h2>No Applications yet</h2>
        </div>
    </div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    data(){
        return {
            "student" : {},
            "applications": [],
            "search_application": ""
        }
    },
    async mounted(){
        await this.loadProfile()
        await this.loadApplications()
    },
    methods : {
        async loadProfile(){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/admin/student/${this.$route.params.id}`,{
                    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
                });
                this.student = response.data ;

            } catch (e) {
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                alert(e.response?.data?.message || "Something went wrong");
                this.$router.push("/admin")
            }
        },
        async downloadResume(){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/admin/student/resume/${this.$route.params.id}`,{responseType: "blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

                const url = window.URL.createObjectURL(response.data)
                window.open(url,"_blank")
            }catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                console.log(e.response);
                
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
                // this.$router.push("/admin")
            }
        },
        async loadApplications(){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/admin/student/applications/${this.$route.params.id}`, {headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})
                this.applications = response.data
                console.log(this.applications);
            } catch (e) {
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
        formatDate(dateString){
            return new Date(dateString).toLocaleString("en-GB")
        },
        async download_offer_letter(application_id){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/admin/application/${application_id}/offer_letter`,{responseType: "blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

                const url = window.URL.createObjectURL(response.data)
                window.open(url,"_blank")
            }catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                // console.log(e.response);
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        }
    },
    computed : {
        filteredApplications(){
            return this.applications.filter(appl =>
                appl.company_name.toLowerCase().includes(this.search_application.toLowerCase())
                ||
                appl.status.toLowerCase().includes(this.search_application.toLowerCase())
            )
        }
    }

    
}

</script>