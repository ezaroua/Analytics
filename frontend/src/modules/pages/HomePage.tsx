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

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            // TODO: Implémenter l'envoi du fichier à l'API
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
                            />
                        </label>
                        {file && <p className="mt-2">Fichier sélectionné : {file.name}</p>}
                    </div>
                </div>
            </div>

            {results && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-xl font-semibold mb-4">Résultats de l'analyse</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Statistiques */}
                        <div>
                            <h4 className="font-medium mb-2">Statistiques</h4>
                            {/* TODO: Afficher les statistiques */}
                        </div>

                        {/* Anomalies */}
                        <div>
                            <h4 className="font-medium mb-2">Anomalies détectées</h4>
                            {/* TODO: Afficher les anomalies */}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HomePage;