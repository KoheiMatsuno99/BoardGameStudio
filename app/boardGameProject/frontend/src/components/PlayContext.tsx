import React from "react";

interface PlayContextProps {
    doesPlay: boolean;
    setDoesPlay: React.Dispatch<React.SetStateAction<boolean>>;
}

interface PlayProviderProps {
    children: React.ReactNode;
}

export const PlayContext = React.createContext<PlayContextProps | undefined>(undefined);

export const PlayProvider = ({ children }: PlayProviderProps) => {
    const [doesPlay, setDoesPlay] = React.useState<boolean>(false);

    return (
        <PlayContext.Provider value={{ doesPlay, setDoesPlay }}>
            {children}
        </PlayContext.Provider>
    );
};