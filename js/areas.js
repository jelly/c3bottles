/**
 * A GeoJSON object containing all the building levels as polygons.
 *
 */
var levels = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"level": 0},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-999, -999], [999, -999], [-999, 999],[999, 999]
                ]]
            }
        }
    ]
};

/**
 * A GeoJSON object containing all the rooms within the building.
 *
 */
var rooms = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Field",
                "level": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-999, -999], [999, -999], [-999, 999],[999, 999]
                ]]
            }
        },

        }
    ]
};

/*
 * Checks whether a point lies within a polygon.
 *
 */
function point_in_polygon(poly, point) {
    for (var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i) {
        if (((poly[i][0] <= point[0] && point[0] < poly[j][0]) || (poly[j][0] <= point[0] && point[0] < poly[i][0])) &&
            (point[1] < (poly[j][1] - poly[i][1]) * (point[0] - poly[i][0]) / (poly[j][0] - poly[i][0]) + poly[i][1])) {
            (c = !c);
        }
    }
    return c;
}

/*
 * Gets the building level for a point by checking all possible level polygons.
 * Returns the level number if the point is within a level or null if it is
 * in none.
 *
 */
exports.get_level = function(point) {
    for (var i in levels.features) {
        if (point_in_polygon(levels.features[i].geometry.coordinates[0], point)) {
            return levels.features[i].properties.level;
        }
    }
    return null;
};

/*
 * Gets the room for a point by checking all possible room polygons.
 * Returns the room properties if the point is within a room or null if it is
 * in none.
 *
 */
exports.get_room = function(point) {
    for (var i in rooms.features) {
        if (point_in_polygon(rooms.features[i].geometry.coordinates[0], point)) {
            return rooms.features[i].properties;
        }
    }
    return null;
};

/* vim: set expandtab ts=4 sw=4: */
