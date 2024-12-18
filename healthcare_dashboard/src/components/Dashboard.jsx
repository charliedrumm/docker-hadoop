import { useState, useEffect, useRef } from "react";
import sampleData from "../data/mapreduce.json";

const Dashboard = () => {
  const [selectedDiseases, setSelectedDiseases] = useState(["Any"]);
  const [selectedSymptoms, setSelectedSymptoms] = useState(["Any"]);
  const [outcome, setOutcome] = useState("Any");
  const [count, setCount] = useState("Any");
  const [data, setData] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef(null);

  // Dropdown options
  const symptomsOptions = ["Any", "No Symptoms", "Fever", "Cough", "Fatigue", "Difficulty Breathing"];
  const outcomesOptions = ["Any", "Positive", "Negative", "None"];
  
  // Sort diseases alphabetically
  const diseasesOptions = ["Any", ...new Set(
    sampleData.data.analysis
      .map((item) => item.disease)
      .filter(disease => disease && disease.trim() !== "") 
  )]
  .sort((a, b) => {
    if (a === "Any") return -1;
    if (b === "Any") return 1;
    return a.localeCompare(b);
  });
  
  // Filter diseases based on search term
  const filteredDiseases = diseasesOptions.filter(disease =>
    disease.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Load initial data
  useEffect(() => {
    setData(sampleData.data.analysis);
  }, []);

  // Click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleDiseaseSelect = (disease) => {
    setSelectedDiseases(prev => {
      if (disease === "Any") {
        return ["Any"];
      }
      
      const newSelection = prev.includes(disease)
        ? prev.filter(d => d !== disease)
        : [...prev.filter(d => d !== "Any"), disease];
        
      return newSelection.length === 0 ? ["Any"] : newSelection;
    });
  };

  const removeDisease = (diseaseToRemove) => {
    setSelectedDiseases(prev => {
      const newSelection = prev.filter(disease => disease !== diseaseToRemove);
      return newSelection.length === 0 ? ["Any"] : newSelection;
    });
  };

  const handleSymptomChange = (symptom) => {
    setSelectedSymptoms(prev => {
      if (symptom === "Any") {
        return ["Any"];
      }
      
      const newSelection = prev.includes(symptom)
        ? prev.filter(s => s !== symptom)
        : [...prev.filter(s => s !== "Any"), symptom];
        
      return newSelection.length === 0 ? ["Any"] : newSelection;
    });
  };

  // Apply filters
  const applyFilters = () => {
    let filteredData = sampleData.data.analysis;

    if (!selectedDiseases.includes("Any")) {
      filteredData = filteredData.filter((item) => 
        selectedDiseases.includes(item.disease)
      );
    }
    
    if (!selectedSymptoms.includes("Any")) {
      filteredData = filteredData.filter((item) => {
        if (selectedSymptoms.includes("No Symptoms")) {
          return item.symptoms.length === 0;
        }
        return selectedSymptoms.some(symptom => 
          item.symptoms.includes(symptom)
        );
      });
    }
    
    if (outcome !== "Any") {
      filteredData = filteredData.filter(
        (item) => item.outcome === outcome || (outcome === "None" && item.outcome === null)
      );
    }
    
    if (count !== "Any") {
      filteredData = filteredData.filter((item) => item.count === parseInt(count, 10));
    }

    setData(filteredData);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Disease Data Viewer</h1>
      
      {/* Filters Section */}
      <section className="space-y-4 mb-8">
        {/* Disease Filter */}
        <div className="space-y-2">
          <h3 className="font-semibold">Diseases:</h3>
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="w-full p-2 text-left bg-white border rounded-md flex justify-between items-center hover:border-blue-500 focus:outline-none focus:border-blue-500"
            >
              <span>Select diseases...</span>
              <span className="transform transition-transform duration-200">
                {isOpen ? '▼' : '▲'}
              </span>
            </button>
            
            {isOpen && (
              <div className="absolute z-10 w-full mt-1 bg-white border rounded-md shadow-lg">
                <input
                  type="text"
                  placeholder="Search diseases..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full p-2 border-b focus:outline-none focus:border-blue-500"
                />
                <div className="max-h-60 overflow-y-auto">
                  {filteredDiseases.map((disease) => (
                    <div
                      key={disease}
                      onClick={() => handleDiseaseSelect(disease)}
                      className={`p-2 cursor-pointer hover:bg-gray-100 flex items-center ${
                        selectedDiseases.includes(disease) ? 'bg-blue-50' : ''
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedDiseases.includes(disease)}
                        onChange={() => {}}
                        className="mr-2"
                      />
                      {disease}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          <div className="flex flex-wrap gap-2 mt-2">
            {selectedDiseases.map(disease => (
              <span
                key={disease}
                className="inline-flex items-center px-2 py-1 rounded-md bg-blue-100 text-blue-800"
              >
                {disease}
                {disease !== "Any" && (
                  <button
                    onClick={() => removeDisease(disease)}
                    className="ml-1 hover:text-blue-600"
                  >
                    ×
                  </button>
                )}
              </span>
            ))}
          </div>
        </div>
  
        {/* Symptoms Filter */}
        <div className="space-y-2">
          <h3 className="font-semibold">Symptoms:</h3>
          <div className="flex flex-wrap gap-2">
            {symptomsOptions.map((symptom) => (
              <label key={symptom} className="inline-flex items-center">
                <input
                  type="checkbox"
                  checked={selectedSymptoms.includes(symptom)}
                  onChange={() => handleSymptomChange(symptom)}
                  className="mr-2"
                />
                <span>{symptom}</span>
              </label>
            ))}
          </div>
        </div>
  
        {/* Outcome Filter */}
        <div className="space-y-2">
          <label className="block">
            <span className="font-semibold">Outcome:</span>
            <select 
              value={outcome}
              onChange={(e) => setOutcome(e.target.value)}
              className="ml-2 p-1 border rounded"
            >
              {outcomesOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
        </div>
  
        {/* Count Filter */}
        <div className="space-y-2">
          <label className="block">
            <span className="font-semibold">Count:</span>
            <input
              type="number"
              value={count}
              placeholder="Any"
              onChange={(e) => setCount(e.target.value || "Any")}
              className="ml-2 p-1 border rounded"
            />
          </label>
        </div>
  
        {/* Apply Filters Button */}
        <button 
          onClick={applyFilters}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          Apply Filters
        </button>
      </section>
  
      {/* Results Section */}
      <section className="mt-8">
        <h2 className="text-xl font-bold mb-4">Results</h2>
        {data.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Disease
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Symptoms
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Outcome
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Count
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.map((item, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{item.disease}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-gray-900">
                        {item.symptoms.length > 0 ? item.symptoms.join(", ") : "No Symptoms"}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-gray-900">{item.outcome || "None"}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      {item.count}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500">No data matches the current filters.</p>
        )}
      </section>
    </div>
  );
};

export default Dashboard;