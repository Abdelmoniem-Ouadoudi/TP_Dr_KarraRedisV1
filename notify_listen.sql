-- Création d'une fonction pour envoyer des notifications via NOTIFY
CREATE OR REPLACE FUNCTION notify_change()
RETURNS TRIGGER AS $$
DECLARE
    payload TEXT;
BEGIN
    -- Construire le message de notification en fonction de l'opération
    IF (TG_OP = 'INSERT') THEN
        payload := FORMAT('INSERT:%s:%s:%s', NEW.id, NEW.devise, NEW.taux);
    ELSIF (TG_OP = 'UPDATE') THEN
        payload := FORMAT('UPDATE:%s:%s:%s', NEW.id, NEW.devise, NEW.taux);
    ELSIF (TG_OP = 'DELETE') THEN
        payload := FORMAT('DELETE:%s', OLD.id);
    END IF;

    -- Envoyer la notification
    PERFORM pg_notify('taux_de_change_channel', payload);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Création d'un déclencheur sur la table `taux_de_change`
CREATE TRIGGER notify_taux_de_change
AFTER INSERT OR UPDATE OR DELETE ON taux_de_change
FOR EACH ROW
EXECUTE FUNCTION notify_change();