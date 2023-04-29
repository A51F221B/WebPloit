import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import CustomizedXAxisTick from "./CustomizedXAxisTick";


function ScanDurationChart() {
  const [scanDurations, setScanDurations] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch("/scan_durations");
        const data = await response.json();
        setScanDurations(data.scan_durations);
      } catch (error) {
        console.error("Error fetching scan durations:", error);
      }
    }
    fetchData();
  }, []);

  return (
    <LineChart width={500} height={300} data={scanDurations}>
      <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
      <XAxis dataKey="scan_id" tick={<CustomizedXAxisTick />} />
      <YAxis
        tick={{ fill: "#666", fontSize: 12 }}
        tickLine={{ stroke: "#ccc" }}
        axisLine={{ stroke: "#ccc" }}
      />
      <Tooltip
        contentStyle={{ backgroundColor: "#f0f8ff", borderRadius: "5px" }}
        labelStyle={{ color: "black", fontWeight: "bold" }}
        itemStyle={{ color: "#82ca9d" }}
      />
      <Legend />
      <Line type="monotone" dataKey="duration" stroke="#82ca9d" />
    </LineChart>
  );
}

export default ScanDurationChart;
