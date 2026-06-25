<template>
  <div>
    <h1>Create Job Posting</h1>

    <label>Title</label><br>
    <input v-model="title" type="text" placeholder="Job Title"><br><br>

    <label>Description</label><br>
    <textarea v-model="description" placeholder="Job Description"></textarea><br><br>

    <label>Package (LPA)</label><br>
    <input v-model="package_amount" type="number" placeholder="Package (LPA)"><br><br>

    <label>Skills Required</label><br>
    <input v-model="skills_required" type="text" placeholder="Python, Vue, SQL"><br><br>

    <label>Minimum CGPA</label><br>
    <input v-model="min_cgpa" type="number" step="0.1" placeholder="Minimum CGPA"><br><br>

    <label>Job Location</label><br>
    <input v-model="job_location" type="text" placeholder="Location"><br><br>

    <label>Vacancies</label><br>
    <input v-model="vacancies" type="number" placeholder="Vacancies"><br><br>

    <label>Deadline</label><br>
    <input v-model="deadline" type="datetime-local" :min="minDeadline"><br><br>

    <button @click="createJobPosting">Create Job Posting</button>
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
        alert(error.response?.data?.message || "Something went wrong")
      }
    }
  }
}
</script>
