import Draw from 'ol/interaction/Draw';
import Map from 'ol/Map';
import View from 'ol/View';
import {OSM, Vector as VectorSource} from 'ol/source';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {defaults as defaultControls} from 'ol/control';

import MousePosition from 'ol/control/MousePosition';
import {createStringXY} from 'ol/coordinate';

const mousePositionControl = new MousePosition({
  coordinateFormat: createStringXY(4),
  projection: 'EPSG:4326',

  className: 'custom-mouse-position',
  target: document.getElementById('mouse-position'),
});

const raster = new TileLayer({
  source: new OSM(),
});

const source = new VectorSource({wrapX: false});

const vector = new VectorLayer({
  source: source,
});

const map = new Map({
  layers: [raster, vector],
  controls: defaultControls().extend([mousePositionControl]),
  target: 'map',
  view: new View({
    center: [302503, 598683],
    zoom: 4,
  }),
});


const projectionSelect = document.getElementById('projection');
projectionSelect.addEventListener('change', function (event) {
  mousePositionControl.setProjection(event.target.value);
});

const precisionInput = document.getElementById('precision');
precisionInput.addEventListener('change', function (event) {
  const format = createStringXY(event.target.valueAsNumber);
  mousePositionControl.setCoordinateFormat(format);
});

const typeSelect = document.getElementById('type');

let draw; // global so we can remove it later
function addInteraction() {
  const value = typeSelect.value;
  if (value !== 'None') {
    draw = new Draw({
      source: source,
      type: typeSelect.value,
    });
    map.addInteraction(draw);
  }
}


typeSelect.onchange = function () {
  map.removeInteraction(draw);
  addInteraction();
};

document.getElementById('type').addEventListener('click', function () {
  map.removeInteraction(draw);
  addInteraction();
});

document.getElementById('undo').addEventListener('click', function () {
  draw.removeLastPoint();
});

document.getElementById('clear').addEventListener('click', function () {
  map.removeInteraction(draw);
  vector.getSource().clear()
  
});



