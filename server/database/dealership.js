const mongoose = require("mongoose");

const dealershipSchema = new mongoose.Schema(
  {
    id: { type: Number, required: true, unique: true, index: true },
    city: { type: String, required: true },
    state: { type: String, required: true, index: true },
    st: { type: String, required: true, uppercase: true, index: true },
    address: { type: String, required: true },
    zip: { type: String, required: true },
    lat: { type: Number, required: true },
    long: { type: Number, required: true },
    short_name: { type: String, default: "" },
    full_name: { type: String, required: true },
  },
  { versionKey: false }
);

module.exports = mongoose.model("dealerships", dealershipSchema);
