let topojson = require("topojson")
let world = require('./aus.topo.json')

let obj = world.objects.aus.geometries
let neighbors = topojson.neighbors(obj)

borders = {}

for (let i = 0; i < neighbors.length; i++) {
    let to_check = neighbors[i]
    let touching = []
    for (let j = 0; j < to_check.length; j++) {
        touching.push(world.objects.aus.geometries[to_check[j]].properties.id)

    }
    borders[world.objects.aus.geometries[i].properties.id] = touching
}

console.log(borders)