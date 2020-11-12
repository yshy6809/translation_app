<template>
    <div>
        <p>主页</p>
        <!--
        <p>随机数：{{ randomNumber }}</p>
        <a-button @click="getRandom" type="primary">生成</a-button>
        -->
        <div>
            <p>文件：<a-input-number id="file_id" v-model="file_id" />
                <a-button @click="getFile" type='primary'>获取</a-button>
            </p>
        </div>
        <a-list item-layout="horizontal" :data-source="text_flows" :pagination="pagination">
            <a-list-item slot="renderItem" slot-scope="item">
                <a-card hoverable style="width: 50%;text-align: 'left'">
                    {{ item.src_text }}
                </a-card>
            </a-list-item>
        </a-list>
    </div>
</template>

<script>
import axios from 'axios'

var text_flows = []
export default {
    data () {
        return {
            randomNumber: 0,
            file_id: 0,
            text_flows,
            pagination: {
                pageSize: 20
            }
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
        getFile() {
            const path = 'http://localhost:5000/api/file/get/' + this.file_id
            axios.get(path).then(response => {
                console.log(response)
                this.text_flows = response.data.text_flows
            })
        },
        created () {
            this.getRandom()
        }
    }
}
</script>