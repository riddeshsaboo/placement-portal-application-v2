<template>
  <div>
    <nav class="p-2 bg-body-tertiary">
        <router-link class="navbar-brand" to="/">
            <h3 class="fw-bold">Placement Portal V2</h3>
        </router-link>
    </nav>
    <div class="container d-flex justify-content-center align-items-center mt-3" style="min-height:85vh">
        <div style="width:420px" class="p-3 bg-body-tertiary rounded border border-info">
            <div class="card-header text-center">
                <h2>Add Job Posting</h2>
            </div>
            <hr>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">Title</label><br>
                    <input v-model="title" type="text" placeholder="Job Title" class="form-control" >
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label><br>
                    <textarea v-model="description" placeholder="Job Description" class="form-control"></textarea>
                </div>
                <div class="mb-3">
                    <label class="form-label">Package (LPA)</label><br>
                    <input v-model="package_amount" type="number" placeholder="Package (LPA)" class="form-control">
                </div>
                <div class="mb-3">
                    <label>Skills Required</label><br>
                    <input v-model="skills_required" type="text" placeholder="Python, Vue, SQL">
                </div>
                <div class="mb-3">
                  <label>Minimum CGPA</label><br>
                  <input v-model="min_cgpa" type="number" step="0.1" placeholder="Minimum CGPA">
                </div>  
                <div class="mb-3">
                  <label>Job Location</label><br>
                  <input v-model="job_location" type="text" placeholder="Location">
                </div>
                <div class="mb-3">
                  <label>Vacancies</label><br>
                  <input v-model="vacancies" type="number" placeholder="Vacancies" min="1">
                </div>
                <div class="mb-3">
                  <label>Deadline</label><br>
                  <input v-model="deadline" type="datetime-local" :min="minDeadline">
                </div>
                <button @click="createJobPosting" class="btn btn-info mt-2 w-100">Create Job Posting</button>
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
      title: "",
      description: "",
      package_amount: "",
      skills_required: "",
      min_cgpa: "",
      job_location: "",
      vacancies: 1,
      deadline: "",
      minDeadline: ""
    }
  },
  mounted() {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, "0")
    const day = String(now.getDate()).padStart(2, "0")
    const hours = String(now.getHours()).padStart(2, "0")
    const minutes = String(now.getMinutes()).padStart(2, "0")
    this.minDeadline = `${year}-${month}-${day}T${hours}:${minutes}`
  },
  methods: {
    async createJobPosting() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/company/addjobposting",
          {
            title: this.title,
            description: this.description,
            salary: this.package_amount,
            skills_required: this.skills_required,
            min_cgpa: this.min_cgpa,
            job_location: this.job_location,
            deadline: this.deadline,
            vacancies: this.vacancies
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`
            }
          }
        )
        alert(response.data.message)
        this.$router.push("/company")
      } catch (error) {
        console.log(error);
        
        alert(error.response?.data?.message || "Something went wrong")
      }
    }
  }
}
</script>
