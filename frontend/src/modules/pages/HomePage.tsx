import { Upload } from 'lucide-react';
import { useState } from 'react';

interface AnalysisResults {
    statistiques?: {
        prix: { moyenne: number; mediane: number; ecart_type: number };
        quantite: { moyenne: number; mediane: number; ecart_type: number };
        note: { moyenne: number; mediane: number; ecart_type: number };
    };
    anomalies?: {
        prix: string[];
        quantite: string[];
        note: string[];
    };
}

const HomePage = () => {
    const [file, setFile] = useState<File | null>(null);
    const [results, setResults] = useState<AnalysisResults | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            try {
                setLoading(true);
                setError(null);
                const file = e.target.files[0];
                setFile(file);

                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch('https://ew6ynrp7i6.execute-api.eu-west-3.amazonaws.com/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                setResults(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Une erreur est survenue');
                console.error('Upload error:', err);
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-8">DataFlow Analytics</h1>

            <div className="mb-8">
                <h2 className="text-2xl font-bold mb-4">Analyse de données CSV</h2>

                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <div className="flex flex-col items-center">
                        <Upload className="w-12 h-12 text-gray-400 mb-4" />
                        <label className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                            Sélectionner un fichier CSV
                            <input
                                type="file"
                                accept=".csv"
                                onChange={handleFileUpload}
                                className="hidden"
                                disabled={loading}
                            />
                        </label>
                        {file && <p className="mt-2">Fichier sélectionné : {file.name}</p>}
                        {loading && <p className="mt-2">Chargement en cours...</p>}
                        {error && <p className="mt-2 text-red-500">{error}</p>}
                    </div>
                </div>
            </div>

            {results && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-xl font-semibold mb-4">Résultats de l'analyse</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <h4 className="font-medium mb-2">Statistiques</h4>
                            {results.statistiques && (
                                <div className="space-y-4">
                                    {Object.entries(results.statistiques).map(([key, stats]) => (
                                        <div key={key} className="border p-4 rounded">
                                            <h5 className="font-medium capitalize">{key}</h5>
                                            <p>Moyenne: {stats.moyenne.toFixed(2)}</p>
                                            <p>Médiane: {stats.mediane.toFixed(2)}</p>
                                            <p>Écart-type: {stats.ecart_type.toFixed(2)}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div>
                            <h4 className="font-medium mb-2">Anomalies détectées</h4>
                            {results.anomalies && (
                                <div className="space-y-4">
                                    {Object.entries(results.anomalies).map(([key, ids]) => (
                                        <div key={key} className="border p-4 rounded">
                                            <h5 className="font-medium capitalize">{key}</h5>
                                            {ids.length > 0 ? (
                                                <ul className="list-disc pl-4">
                                                    {ids.map(id => (
                                                        <li key={id}>ID: {id}</li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p>Aucune anomalie détectée</p>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HomePage;