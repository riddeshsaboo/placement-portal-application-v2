<template>
<div>
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
          <router-link to="/admin" class="text-decoration-none text-dark fs-3 fw-bold">Admin Dashboard</router-link>
      </div>
    </nav> 
    <router-link to="/admin" class="btn btn-outline-secondary m-3">← Back</router-link>
    <div class="card m-3 border border-dark">
        <div class="card-header">
            <span class="m-2 fw-bold fs-4">Company Details</span>
        </div>
        <div class="card-body">
            <table class="table m-2">
                <tr class="my-2">
                    <th width="220">Company Name</th>
                    <td>{{ company.company_name }}</td>
                </tr>
                <tr class="my-2">
                    <th>Industry</th>
                    <td>{{ company.industry }}</td>
                </tr>
                <tr class="my-2">
                    <th>Description</th>
                    <td>{{ company.description || "Not Provided" }}</td>
                </tr>
                <tr class="my-2">
                    <th>Website</th>
                    <td>
                        <a v-if="company.website" :href="company.website" target="_blank">
                            {{ company.website }}
                        </a>
                        <span v-else class="fw-bold">Not Provided</span>
                    </td>
                </tr>
                <tr class="my-2">
                    <th>Location</th>
                    <td>{{ company.location || "Not Provided" }}</td>
                </tr>
                <tr class="my-2">
                    <th>Status</th>
                    <td>
                        <span v-if="company.approval_status == 'pending'" class="badge bg-warning">Pending</span>
                        <span v-else-if="company.approval_status == 'approved'" class="badge bg-success">Approved</span>
                        <span v-else-if="company.approval_status == 'blacklisted'" class="badge bg-dark text-white">Blacklisted</span>
                        <span v-else-if="company.approval_status == 'rejected'" class="badge bg-danger">Rejected</span>
                    </td>
                </tr>
                <tr class="my-2">
                    <th>Actions</th>
                    <td>
                        <button v-if="company.approval_status == 'pending'" @click="update_company_status(company.id,'approved')" class="btn btn-success btn-sm bg-success m-2">Approve</button>
                        <button v-if="company.approval_status == 'pending'" @click="update_company_status(company.id,'rejected')" class="btn btn-danger btn-sm bg-danger m-2">Reject</button>
                        <button v-if="company.approval_status == 'approved'" @click="update_company_status(company.id,'blacklisted')" class="btn btn-danger btn-sm bg-danger m-2">Blacklist</button>
                        <button v-if="company.approval_status == 'rejected'" @click="update_company_status(company.id,'approved')" class="btn btn-success btn-sm bg-success m-2">Approve</button>
                        <button v-if="company.approval_status == 'blacklisted'" @click="update_company_status(company.id,'approved')" class="btn btn-success btn-sm bg-success m-2">Unblacklist</button>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div class="card m-3 border border-dark">
        <div v-if="job_postings.length > 0">
        <div class="card-header">
            <span class="m-2 fw-bold fs-4">Job Postings</span>
        </div>
        <div class="input-group m-1 mt-3 row">
            <div class="col-md-6">
                <input type="search" v-model="search_job" placeholder="Search Job postings by title / status" class="form-control border border-dark" />
            </div>
        </div>
        <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
            <table class="table table-hover">
                <thead class="table-warning">
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Salary</th>
                        <th>Min CGPA</th>
                        <th>Skills required</th>
                        <th>Vacancies</th>
                        <th>Created at</th>
                        <th>Deadline</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(posting, index) in filteredJobs" :key="posting.id">
                        <td>{{ index+1 }}</td>
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
                        <td>
                            <div class="d-flex gap-2">
                            <button v-if="posting.status == 'pending'" @click="updatePostingStatus(posting.id,'approved')" class="btn btn-success btn-sm " >Approve</button>
                            <button v-if="posting.status == 'pending'" @click="updatePostingStatus(posting.id,'rejected')" class="btn btn-danger btn-sm "> Reject</button>
                            <button v-if="posting.status == 'approved'" @click="updatePostingStatus(posting.id,'closed')" class="btn btn-danger btn-sm "> Close</button>
                            <span v-if="posting.status == 'closed'">NA</span>
                            <span v-if="posting.status == 'rejected'">NA</span>
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

</div>
</template>

<script>
import axios from "axios"

export default{
    data(){
        return{
            company:{},
            job_postings: [], 
            search_job: ""
        }
    },

    async mounted(){
        await this.loadCompany()
        await this.loadJobPostings()
    },

    methods:{
        async loadCompany(){
            const response = await axios.get(`http://127.0.0.1:5000/admin/company/${this.$route.params.id}`,{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
            this.company = response.data
            // console.log(this.company);
        },
        async update_company_status(company_id,status){
            await axios.put(`http://127.0.0.1:5000/admin/company/${company_id}/status`,{status : status},{headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})

            await this.loadCompany()
        },
        async loadJobPostings(){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/admin/company/job_postings/${this.$route.params.id}`,{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                this.job_postings = response.data
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
        formatDate(dateString){
            return new Date(dateString).toLocaleString("en-GB")
        },
        async updatePostingStatus(posting_id,status){
            await axios.put(`http://127.0.0.1:5000/admin/job_posting/${posting_id}/status`,{status: status},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
            await this.loadJobPostings()
            await this.loadData()
        }

    },

    computed : {
        filteredJobs(){
            return this.job_postings.filter(job =>
                job.title.toString().toLowerCase().includes(this.search_job.toLowerCase())
                ||
                job.status.toLowerCase().includes(this.search_job.toLowerCase())
            )
        }
    }
}
</script>