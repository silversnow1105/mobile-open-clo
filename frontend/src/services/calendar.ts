import api from "./api";

export const calendarService = {
  getEvents: (startDate: string, endDate: string) =>
    api.get("/api/calendar/events", { params: { start_date: startDate, end_date: endDate } }),

  syncCalendar: (accessToken: string) =>
    api.post("/api/calendar/sync", { access_token: accessToken }),
};
