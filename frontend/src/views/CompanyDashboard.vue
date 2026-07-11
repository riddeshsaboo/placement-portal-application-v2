<template>
    <div v-if="role == 'company' " class="m-2">
        <nav class="navbar bg-body-tertiary">
            <div class="container-fluid">
                <h3 class="fw-bold">Company Dashboard</h3>
                <div>
                    <router-link to="/company/add_job_posting" class="btn btn-info fw-bold">Add Job posting</router-link>
                    <button v-if="!showchart" class="btn btn-warning m-1" @click="()=>{showchart = !showchart}">Show Chart</button>
                    <button v-else class="btn btn-warning m-1" @click="()=>{showchart = !showchart}">Hide Chart</button>
                    <button class="btn btn-success" @click="exportCSV">Export Applications CSV</button>
                    <button v-if="export_ready" class="btn btn-primary ms-2" @click="downloadCSV">Download CSV</button>
                    <button class="btn btn-danger m-1" @click="logout">Logout </button>
                </div>
            </div>
        </nav> 
        <div class="card mb-3 mt-3 ">
            <div class="card-header">
                <span class="fw-bold">Welcome! {{company_name}}</span>
            </div>
        </div>
        <div class="row g-3 mb-4">
            <div class="col-md">
                <div class="card border-success h-100">
                    <div class="card-body text-center">
                        <h5 class="text-success">Total Job Postings</h5>
                        <h2 class="fw-bold">{{ total_job_postings }}</h2>
                        <hr>
                        <h5 class="text-success">Active Job Postings</h5>
                        <h2 class="fw-bold">{{ active_job_postings }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md">
                <div class="card border-primary h-100">
                    <div class="card-body text-center">
                        <h5 class="text-primary">Pending Job Postings</h5>
                        <h2 class="fw-bold">{{ pending_job_postings }}</h2>
                        <hr>
                        <h5 class="text-primary">Closed Job Postings</h5>
                        <h2 class="fw-bold">{{ closed_job_postings }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md">
                <div class="card border-warning h-100">
                    <div class="card-body text-center">
                        <h5 class="text-warning">Received Applications</h5>
                        <h2 class="fw-bold">{{ received_applications }}</h2>
                        <hr>
                        <h5 class="text-warning">Placed Candidates</h5>
                        <h2 class="fw-bold">{{ placed_candidates }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md">
                <div class="card border-danger h-100">
                    <div class="card-body text-center">
                        <h5 class="text-danger">Selected Candidates</h5>
                        <h2 class="fw-bold">{{ selected_candidates }}</h2>
                        <hr>
                        <h5 class="text-danger">Rejected Candidates</h5>
                        <h2 class="fw-bold">{{ rejected_candidates }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md">
                <div class="card border-info h-100">
                    <div class="card-body text-center">
                        <h5 class="text-info">Shortlisted Candidates</h5>
                        <h2 class="fw-bold">{{ shortlisted_candidates }}</h2>
                        <hr>
                        <h5 class="text-info">Interview Scheduled Candidates</h5>
                        <h2 class="fw-bold">{{ interview_scheduled_candidates }}</h2>
                    </div>
                </div>
            </div>
        
    </div>

    <div v-if="showchart" class="container m-5">
        <div class="card shadow">
            <div class="card-body">
                <Bar :data="dashboardData" :options="chartOptions"/>
            </div>
        </div>
    </div>

    <div v-if="job_postings.length > 0" id="job_postings">
            <h2>Job Postings</h2>
            <div class="input-group m-2">
                <input type="search" v-model="search_job" placeholder="Search Job postings by title / company name / status" class="form-control" style="max-width: 370px"  />
            </div>
            <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
                <table class="table table-hover">
                    <thead class="table-success">
                        <tr>
                            <th>Sr No</th>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Salary (LPA)</th>
                            <th>Min CGPA</th>
                            <th>Skills required</th>
                            <th>Vacancies</th>
                            <th>Created at</th>
                            <th>Deadline</th>
                            <th>Status</th>
                            <th>Applications</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(posting, index) in filteredJobs" :key="posting.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ posting.id }}</td>
                            <td>{{ posting.title }}</td>
                            <td>{{ posting.salary || "Not Disclosed" }}</td>
                            <td>{{ posting.min_cgpa || "Not Disclosed"}}</td>
                            <td>{{ posting.skills_required || "Not Disclosed" }}</td>
                            <td>{{ posting.vacancies }}</td>
                            <td>{{ formatDate(posting.created_at) }}</td>
                            <td>{{ formatDate(posting.deadline) }}</td>
                            <td>
                                <span v-if="posting.status == 'pending'" class="badge bg-warning">Pending</span>
                                <span v-if="posting.status == 'approved'" class="badge bg-success">Approved</span>
                                <span v-if="posting.status == 'closed'" class="badge bg-danger">Closed</span>
                                <span v-if="posting.status == 'rejected'" class="badge bg-danger">Rejected</span>
                            </td>
                            <td>{{ posting.applications }}</td>
                            <td>
                                <div class="d-flex gap-2">
                                <!-- <button v-if="posting.status == 'approved'" @click="updatePostingStatus(posting.id,'closed')" class="btn btn-danger btn-sm "> Close</button> -->
                                <router-link :to="`/company/job_posting/${posting.id}`" class="btn btn-primary btn-sm">Manage</router-link>
                                <!-- <span v-else >NA</span> -->
                                </div>
                            </td>
                        </tr>
                    </tbody>
            </table>
        </div>
    </div>
    <div v-else>
        <br><br>
        <h2>No Job postings yet</h2>
    </div>


</div>
<div v-else>
    <h1>You are not company! Please <router-link to="/login">Login</router-link></h1>
</div>
</template>

<script>
import axios from 'axios';
import {Chart as ChartJS,CategoryScale,LinearScale,BarElement,Title,Tooltip,Legend} from "chart.js";

import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
    data(){
        const role = localStorage.getItem("role");
        const companyId = localStorage.getItem("company_id")
        return {
            role : role ,
            company_id : companyId,
            company_name: "",
            total_job_postings: 0,
            active_job_postings: 0,
            received_applications: 0,
            pending_job_postings: 0,
            closed_job_postings: 0,
            shortlisted_candidates: 0,
            selected_candidates: 0,
            interview_scheduled_candidates: 0,
            job_postings: [],
            search_job: "",
            export_ready: false , 
            placed_candidates : 0,
            rejected_candidates : 0,
            showchart : false 
        }
    },

    async mounted() {
        if (this.role !== "company") {
            if(this.role == "student"){
                this.$router.push("/student")
            }
            else if(this.role == "admin"){
                this.$router.push("/admin")
            }
            else{
                this.$router.push("/login")
            }
        }

        await this.loadDashboard()
        await this.loadJobPostings()

    },

    methods : {
        logout() {
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            localStorage.removeItem("company_id");
            this.$router.push("/login");
        },
        async loadDashboard(){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/company/dashboard/${this.company_id}`,{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
            
                this.company_name = response.data.company_name
                this.total_job_postings = response.data.total_job_postings
                this.active_job_postings = response.data.active_job_postings
                this.received_applications = response.data.received_applications
                this.pending_job_postings = response.data.pending_job_postings
                this.closed_job_postings = response.data.closed_job_postings
                this.shortlisted_candidates = response.data.shortlisted_candidates
                this.selected_candidates = response.data.selected_candidates
                this.interview_scheduled_candidates = response.data.interview_scheduled_candidates
                this.placed_candidates = response.data.placed_candidates
                this.rejected_candidates = response.data.rejected_candidates

                // console.log(response.data)
            } catch (e) {
                console.log(e.response);
                console.log(e.response?.status);
                console.log(e.response?.data);
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

        async loadJobPostings(){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/company/job_postings/${this.company_id}`,{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                this.job_postings = response.data; 
                console.log(this.job_postings)
            } catch (e) {
                console.log(e);
            }
        },
        formatDate(dateString){
            return new Date(dateString).toLocaleString("en-GB")
        },

        async updatePostingStatus(posting_id,status){
            await axios.put(`http://127.0.0.1:5000/company/job_posting/${posting_id}/status`,{status: status},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
            await this.loadJobPostings()
            await this.loadData()
        },
        async exportCSV(){
            try{
                this.export_ready = false
                await axios.post("http://127.0.0.1:5000/company/export",{},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                alert("CSV generated successfully.")
                this.export_ready = true
            }
            catch(e){
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong")
            } 
        },

        async downloadCSV(){
            try{
                const response = await axios.get("http://127.0.0.1:5000/company/export/download",{responseType:"blob", headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                const url = window.URL.createObjectURL(response.data)
                const a = document.createElement("a")
                a.href = url
                a.download = "applications.csv"
                a.click()

                window.URL.revokeObjectURL(url)
            }
            catch(e){
                alert(e.response?.data?.message || "Something went wrong")
            }
        }

    },

    computed : {
        filteredJobs(){
            return this.job_postings.filter(job =>
                job.title.toString().toLowerCase().includes(this.search_job.toLowerCase())
                ||
                job.status.toLowerCase().includes(this.search_job.toLowerCase())
            )
        },

        dashboardData(){
            return{
                labels:["Total Job Postings", "Active Job Postings", "Pending Job Postings", "Closed Job Postings", "Received Applications","Placed Candidates", "Selected Candidates", "Rejected Candidates" , "Shortlisted Candidates","Interview Candidates"],

                datasets:[{
                        label:"Count",
                        data:[this.total_job_postings, this.active_job_postings, this.pending_job_postings, this.closed_job_postings, this.received_applications, this.placed_candidates,this.selected_candidates, this.rejected_candidates,this.shortlisted_candidates, this.interview_scheduled_candidates],
                        backgroundColor:["green", "lightgreen", "blue", "skyblue","orange", "gold","red","tomato", "royalblue", "cyan"],
                }]
            }
        },

        chartOptions(){
            return{
                responsive:true,
                indexAxis:"y",
                plugins:{
                    legend:{display:false},
                    title:{display:true,text: "Company Recruitment Overview"}
                },
                scales:{
                    x:{beginAtZero:true}
                }
            }
        },
    
    },
    components: {
        Bar
    },

    }


</script>