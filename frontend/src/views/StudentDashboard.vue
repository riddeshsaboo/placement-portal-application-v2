<template>
  <div class="container mt-4">
    <h2>Student Dashboard</h2>
    <button class="btn btn-danger mb-3" @click="logOut()">Logout</button>

    <div class="card mt-3">
      <div class="card-header">Available Job Postings</div>
      <div class="card-body">
        <input class="form-control mb-3" placeholder="Search company or job title" v-model="search_job">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Sr</th>
              <th>Company</th>
              <th>Title</th>
              <th>Package</th>
              <th>Minimum CGPA</th>
              <th>Deadline</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, index) in filteredJobs" :key="job.id">
              <td>{{ index + 1 }}</td>
              <td>{{ job.company_name }}</td>
              <td>{{ job.title }}</td>
              <td>{{ job.salary || "Not Disclosed" }}</td>
              <td>{{ job.min_cgpa || "Not Required" }}</td>
              <td>{{ formatDate(job.deadline) }}</td>
              <td><router-link :to="`/student/job_posting/${job.id}`" class="btn btn-primary btn-sm">View</router-link></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card mt-4">
      <div class="card-header">My Applications</div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Sr</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Applied On</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(application, index) in applications" :key="application.id">
              <td>{{ index + 1 }}</td>
              <td>{{ application.company_name }}</td>
              <td>{{ application.title }}</td>
              <td>{{ formatDate(application.applied_at) }}</td>
              <td>
                <span class="badge bg-warning text-dark" v-if="application.status === 'applied'">Applied</span>
                <span class="badge bg-primary" v-else-if="application.status === 'shortlisted' || application.status === 'interview_scheduled'">Shortlisted</span>
                <span class="badge bg-success" v-else-if="application.status === 'selected'">Selected</span>
                <span class="badge bg-success" v-else-if="application.status === 'placed'">Placed</span>
                <span class="badge bg-danger" v-else>Rejected</span>
              </td>
              <td>
                <button class="btn btn-primary m-2" v-if="application.status == 'selected'" @click="accept_offer(application.id)">Accept</button>
                <button class="btn btn-danger m-2" v-if="application.status == 'selected'" @click="reject_offer(application.id)">Reject</button>
                <span v-else class="fw-bold">NA</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      jobs: [],
      search_job: "",
      applications: []
    };
  },
  async mounted() {
    await this.loadJobs();
    await this.loadApplications();
  },
  methods: {
    logOut() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    },
    async loadJobs() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/student/job_postings", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.jobs = response.data;
      } catch (error) {
        console.error("Error loading jobs:", error);
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleString("en-GB");
    },
    async loadApplications() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/student/applications", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.applications = response.data;
      } catch (error) {
        console.error("Error loading applications:", error);
      }
    },

    async accept_offer(application_id){
        try{
            let conf = confirm("Accepting this offer would close all other applications. Are you sure?")
            console.log(application_id)
            if(conf){
                const response = await axios.put(`http://127.0.0.1:5000/student/application/${application_id}/accept`,{},{headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }})
                this.loadApplications()
                alert(response.data.message);
                // console.log(response.data.message);
                
            }
        }catch(e){
            console.log(e);
            alert(e.response?.data?.message || "Something went wrong");
        }
    },

    async reject_offer(application_id){
        try{
            console.log(application_id)
            let conf = confirm("Reject this offer? Are you sure?")
            if(conf){
                const response = await axios.put(`http://127.0.0.1:5000/student/application/${application_id}/reject`,{},{headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }})
                this.loadApplications()
                console.log(response.data.message);
                // alert(response.data.message);
            }
        }catch(e){
            console.log(e);
            alert(e.response?.data?.message || "Something went wrong");
        }
    }
  },
  computed: {
    filteredJobs() {
      const query = this.search_job.toLowerCase();
      return this.jobs.filter(job => 
        job.company_name.toLowerCase().includes(query) || 
        job.title.toLowerCase().includes(query)
      );
    }
  }
};
</script>