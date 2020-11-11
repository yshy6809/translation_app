<template>
    <div>
        <p>主页</p>
        <p>随机数：{{ randomNumber }}</p>
        <button @click="getRandom">Generate</button>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data () {
        return {
            randomNumber: 0
        }
    },
    methods: {
        getRandom() {
            const path = 'http://localhost:5000/api/random'
            axios.get(path)
            .then(response => {
                this.randomNumber = response.data.randomNumber
            })
            .catch(error => {
                console.log(error)
            })
        },
        created () {
            this.getRandom()
        }
    }
}
</script>